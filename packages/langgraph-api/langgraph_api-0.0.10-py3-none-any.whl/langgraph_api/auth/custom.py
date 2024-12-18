import asyncio
import copy
import functools
import importlib.util
import inspect
import os
import sys
from collections.abc import Awaitable, Callable, Mapping
from contextlib import AsyncExitStack
from typing import Any, get_args

import structlog
from langgraph_sdk import Auth
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
    SimpleUser,
)
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response

from langgraph_api.auth.langsmith.backend import LangsmithAuthBackend
from langgraph_api.config import LANGGRAPH_AUTH

logger = structlog.stdlib.get_logger(__name__)

SUPPORTED_PARAMETERS = {
    "request": Request,
    "body": dict,
    "user": BaseUser,
    "path": str,
    "method": str,
    "scopes": list[str],
    "path_params": dict[str, str] | None,
    "query_params": dict[str, str] | None,
    "headers": dict[str, bytes] | None,
    "authorization": str | None,
    "scope": dict[str, Any],
}


def get_custom_auth_middleware() -> AuthenticationBackend:
    """Load authentication function from a Python file or config dict."""
    if not LANGGRAPH_AUTH:
        raise ValueError(
            "LANGGRAPH_AUTH must be set to a Python file path or a config dict"
            " to use custom authentication."
        )
    logger.info("Using custom authentication", langgraph_auth=LANGGRAPH_AUTH)
    return _get_custom_auth_middleware(LANGGRAPH_AUTH)


@functools.lru_cache(maxsize=1)
def get_auth_instance() -> Auth | None:
    logger.info(
        f"Getting auth instance: {LANGGRAPH_AUTH}", langgraph_auth=str(LANGGRAPH_AUTH)
    )
    if not LANGGRAPH_AUTH:
        return None
    path = LANGGRAPH_AUTH.get("path")
    if path is None:
        return None
    return _get_auth_instance(path)


async def handle_event(
    ctx: Auth.types.AuthContext | None,
    value: dict,
) -> Auth.types.FilterType | None:
    """Run all handlers for a request.

    Returns:
    - A FilteredValue with the modified value and any filters to apply
    - Raises HTTPException(403) if any handler rejects the request

    Handlers are run in order from most specific to most general:
    1. Resource+action specific handlers (e.g. "runs", "create")
    2. Resource handlers (e.g. "runs", "*")
    3. Action handlers (e.g. "*", "create")
    4. Global handlers ("*", "*")
    """
    if ctx is None:
        return
    auth = get_auth_instance()
    if auth is None:
        return
    handler = _get_handler(auth, ctx)
    if not handler:
        return

    result = await handler(ctx=ctx, value=value)

    if result in (None, True):
        return
    if result is True:
        raise HTTPException(403, "Forbidden")

    if not isinstance(result, dict):
        raise HTTPException(
            500,
            f"Auth handler returned invalid result. Expected filter dict, None, or boolean. Got {type(result)} instead.",
        )

    return result


class CustomAuthBackend(AuthenticationBackend):
    def __init__(
        self,
        fn: (
            Callable[
                [Request],
                Awaitable[tuple[list[str], Any]],
            ]
            | None
        ) = None,
        disable_studio_auth: bool = False,
    ):
        if fn is None:
            self.fn = None
        elif not inspect.iscoroutinefunction(fn):
            self.fn = functools.partial(run_in_threadpool, fn)
        else:
            self.fn = fn
        self._param_names = (
            get_named_arguments(fn, supported_params=SUPPORTED_PARAMETERS)
            if fn
            else None
        )
        if not disable_studio_auth:
            self.ls_auth = LangsmithAuthBackend()
        else:
            self.ls_auth = None

    def __str__(self):
        return (
            f"CustomAuthBackend(fn={self.fn}, "
            f"ls_auth={self.ls_auth}, "
            f"param_names={self._param_names}"
            ")"
        )

    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, BaseUser] | None:
        if self.ls_auth is not None and (
            (auth_scheme := conn.headers.get("x-auth-scheme"))
            and auth_scheme == "langsmith"
        ):
            return await self.ls_auth.authenticate(conn)
        if self.fn is None:
            return None
        try:
            args = _extract_arguments_from_scope(
                conn.scope, self._param_names, request=Request(conn.scope)
            )
            scopes, user = await self.fn(**args)
            return AuthCredentials(scopes), _normalize_user(user)
        except AssertionError as e:
            raise AuthenticationError(str(e)) from None


def _get_custom_auth_middleware(
    config: str | dict,
) -> AuthenticationBackend:
    disable_studio_auth = False
    if isinstance(config, str):
        path: str | None = config
    else:
        path = config.get("path")
        disable_studio_auth = config.get("disable_studio_auth", disable_studio_auth)
    auth_instance = _get_auth_instance(path)
    result = CustomAuthBackend(
        auth_instance._authenticate_handler if auth_instance else None,
        disable_studio_auth,
    )
    logger.info(f"Loaded custom auth middleware: {str(result)}")
    return result


@functools.lru_cache(maxsize=1)
def _get_auth_instance(path: str | None = None) -> Auth | None:
    if path is not None:
        auth_instance = _load_auth_obj(path)
    else:
        auth_instance = None

    if auth_instance is not None and (
        deps := _get_dependencies(auth_instance._authenticate_handler)
    ):
        auth_instance._authenticate_handler = _solve_fastapi_dependencies(
            auth_instance._authenticate_handler, deps
        )
    logger.info(f"Loaded auth instance from path {path}: {auth_instance}")
    return auth_instance


def _extract_arguments_from_scope(
    scope: dict[str, Any],
    param_names: set[str],
    request: Request | None = None,
    response: Response | None = None,
) -> dict[str, Any]:
    """Extract requested arguments from the ASGI scope (and request/response if needed)."""

    auth = scope.get("auth")
    args: dict[str, Any] = {}
    if "scope" in param_names:
        args["scope"] = scope
    if "request" in param_names and request is not None:
        args["request"] = request
    if "response" in param_names and response is not None:
        args["response"] = response
    if "user" in param_names:
        user = scope.get("user")
        args["user"] = user
    if "scopes" in param_names:
        args["scopes"] = auth.scopes if auth else []
    if "path_params" in param_names:
        args["path_params"] = scope.get("path_params", {})
    if "path" in param_names:
        args["path"] = scope["path"]
    if "query_params" in param_names:
        args["query_params"] = scope.get("query_params", {})
    if "headers" in param_names:
        args["headers"] = dict(scope.get("headers", {}))
    if "authorization" in param_names:
        headers = dict(scope.get("headers", {}))
        authorization = headers.get(b"authorization") or headers.get(b"Authorization")
        if isinstance(authorization, bytes):
            authorization = authorization.decode(encoding="utf-8")
        args["authorization"] = authorization
    if "method" in param_names:
        args["method"] = scope.get("method")

    return args


def _get_dependencies(fn: Callable | None) -> dict[str, Any] | None:
    if fn is None:
        return None
    Depends = _depends()
    if Depends is None:
        # FastAPI not installed
        return

    # For Python versions < 3.10, get_annotations is available via inspect
    # For Python 3.10+, it's built-in. Here we just call it.
    annotations = (
        inspect.get_annotations(fn)
        if hasattr(inspect, "get_annotations")
        else getattr(fn, "__annotations__", {})
    )
    deps = {}
    for arg_name, arg_type in annotations.items():
        for annotation in get_args(arg_type):
            if isinstance(annotation, Depends):
                deps[arg_name] = annotation
                break
    return deps


def _solve_fastapi_dependencies(
    fn: Callable[..., Any], deps: Mapping[str, Any]
) -> Callable:
    """Solve FastAPI dependencies for a given function."""
    logger.info("Solving FastAPI dependencies", fn=str(fn), deps=str(deps))
    from fastapi.dependencies.utils import (
        get_parameterless_sub_dependant,
        solve_dependencies,
    )

    dependents = {
        name: get_parameterless_sub_dependant(depends=dep, path="")
        for name, dep in deps.items()
    }
    for name, dependent in dependents.items():
        if dependent.call is None:
            raise ValueError(
                f"FastAPI-defined dependencies must have a callable dependency. No dependency found for {name} in {fn}."
            )

    is_async = inspect.iscoroutinefunction(fn)

    _param_names = {
        k
        for k in get_named_arguments(
            fn, supported_params=SUPPORTED_PARAMETERS | dict(deps)
        )
        if k not in dependents
    }

    async def decorator(scope: dict, request: Request):
        async with AsyncExitStack() as stack:
            all_solved = await asyncio.gather(
                *(
                    solve_dependencies(
                        request=request,
                        dependant=dependent,
                        async_exit_stack=stack,
                        embed_body_fields=False,
                    )
                    for dependent in dependents.values()
                )
            )
            all_injected = await asyncio.gather(
                *(
                    _run_async(dependent.call, solved.values, is_async)
                    for dependent, solved in zip(
                        dependents.values(), all_solved, strict=False
                    )
                )
            )
            kwargs = {
                name: value
                for name, value in zip(dependents.keys(), all_injected, strict=False)
            }
            other_params = _extract_arguments_from_scope(
                scope, _param_names, request=request
            )
            return await fn(**(kwargs | other_params))

    return decorator


@functools.lru_cache(maxsize=1)
def _depends() -> Any:
    try:
        from fastapi.params import Depends

        return Depends
    except ImportError:
        return None


class DotDict:
    def __init__(self, dictionary: dict[str, Any]):
        self._dict = dictionary
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DotDict(value))
            else:
                setattr(self, key, value)

    def __getattr__(self, name):
        if name not in self._dict:
            raise AttributeError(f"'DotDict' object has no attribute '{name}'")
        return self._dict[name]

    def __deepcopy__(self, memo):
        return DotDict(copy.deepcopy(self._dict))

    def dict(self):
        return self._dict


class ProxyUser(BaseUser):
    """A proxy that wraps a user object to ensure it has all BaseUser properties.

    This will:
    1. Ensure the required identity property exists
    2. Provide defaults for optional properties if they don't exist
    3. Proxy all other attributes to the underlying user object
    """

    def __init__(self, user: Any):
        if not hasattr(user, "identity"):
            raise ValueError("User must have an identity property")
        self._user = user

    @property
    def identity(self) -> str:
        return self._user.identity

    @property
    def is_authenticated(self) -> bool:
        return getattr(self._user, "is_authenticated", True)

    @property
    def display_name(self) -> str:
        return getattr(self._user, "display_name", self.identity)

    def __deepcopy__(self, memo):
        return ProxyUser(copy.deepcopy(self._user))

    def model_dump(self):
        if hasattr(self._user, "model_dump") and callable(self._user.model_dump):
            return {
                "identity": self.identity,
                "is_authenticated": self.is_authenticated,
                "display_name": self.display_name,
                **self._user.model_dump(mode="json"),
            }
        return self.dict()

    def dict(self):
        d = (
            self._user.dict()
            if hasattr(self._user, "dict") and callable(self._user.dict)
            else {}
        )
        return {
            "identity": self.identity,
            "is_authenticated": self.is_authenticated,
            "display_name": self.display_name,
            **d,
        }

    def __getattr__(self, name: str) -> Any:
        """Proxy any other attributes to the underlying user object."""
        return getattr(self._user, name)


def _normalize_user(user: Any) -> BaseUser:
    """Normalize user into a BaseUser instance."""
    if isinstance(user, BaseUser):
        return user
    if hasattr(user, "identity"):
        return ProxyUser(user)
    if isinstance(user, str):
        return SimpleUser(username=user)
    if isinstance(user, dict) and "identity" in user:
        return ProxyUser(DotDict(user))
    raise ValueError(
        f"Expected a BaseUser instance with required property: identity (str). "
        f"Optional properties are: is_authenticated (bool, defaults to True) and "
        f"display_name (str, defaults to identity). Got {type(user)} instead"
    )


def _load_auth_obj(path: str) -> Auth:
    """Load an object from a path string."""
    if ":" not in path:
        raise ValueError(
            f"Invalid auth path format: {path}. "
            "Must be in format: './path/to/file.py:name' or 'module:name'"
        )

    module_name, callable_name = path.rsplit(":", 1)
    module_name = module_name.rstrip(":")

    try:
        if "/" in module_name or ".py" in module_name:
            # Load from file path
            modname = f"dynamic_module_{hash(module_name)}"
            modspec = importlib.util.spec_from_file_location(modname, module_name)
            if modspec is None or modspec.loader is None:
                raise ValueError(f"Could not load file: {module_name}")
            module = importlib.util.module_from_spec(modspec)
            sys.modules[modname] = module
            modspec.loader.exec_module(module)
        else:
            # Load from Python module
            module = importlib.import_module(module_name)

        loaded_auth = getattr(module, callable_name, None)
        if loaded_auth is None:
            raise ValueError(
                f"Could not find auth '{callable_name}' in module: {module_name}"
            )
        if not isinstance(loaded_auth, Auth):
            raise ValueError(f"Expected an Auth instance, got {type(loaded_auth)}")
        return loaded_auth

    except ImportError as e:
        e.add_note(f"Could not import module:\n{module_name}\n\n")
        if os.environ.get("LANGSMITH_LANGGRAPH_API_VARIANT") == "local_dev":
            e.add_note(
                "If you're in development mode, make sure you've installed your project "
                "and its dependencies:\n"
                "- For requirements.txt: pip install -r requirements.txt\n"
                "- For pyproject.toml: pip install -e .\n"
            )
        raise
    except FileNotFoundError as e:
        raise ValueError(f"Could not find file: {module_name}") from e


async def _run_async(
    dep_call: Callable[..., Any], values: dict[str, Any], is_coroutine: bool
) -> Any:
    """Run a dependency call either in threadpool or directly if async."""
    if is_coroutine:
        return await dep_call(**values)
    return await run_in_threadpool(dep_call, **values)


def _get_handler(auth: Auth, ctx: Auth.types.AuthContext) -> Auth.types.Handler | None:
    """Get the most specific handler for a resource and action."""
    key = (ctx.resource, ctx.action)
    if key in auth._handler_cache:
        return auth._handler_cache[key]
    keys = [
        (ctx.resource, ctx.action),  # most specific
        (ctx.resource, "*"),  # resource-specific
        ("*", ctx.action),  # action-specific
        ("*", "*"),  # most general
    ]
    for key in keys:
        if key in auth._handlers:
            result = auth._handlers[key][
                -1
            ]  # Get the last defined, most specific handler
            auth._handler_cache[key] = result
            return result
    if auth._global_handlers:
        return auth._global_handlers[-1]

    return None


def get_named_arguments(fn: Callable, supported_params: dict) -> set[str]:
    """Get the named arguments that a function accepts, ensuring they're supported."""
    sig = inspect.signature(fn)
    # Check for unsupported required parameters
    unsupported = []
    for name, param in sig.parameters.items():
        if name not in supported_params and param.default is param.empty:
            unsupported.append(name)

    if unsupported:
        supported_str = "\n".join(
            f"  - {name} ({getattr(typ, '__name__', str(typ))})"
            for name, typ in supported_params.items()
        )
        raise ValueError(
            f"Handler has unsupported required parameters: {', '.join(unsupported)}.\n"
            f"Supported parameters are:\n{supported_str}"
        )

    return {p for p in sig.parameters if p in supported_params}
