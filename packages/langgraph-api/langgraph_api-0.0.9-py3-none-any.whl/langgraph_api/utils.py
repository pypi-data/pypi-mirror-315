import contextvars
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Protocol, TypeAlias, TypeVar

from langgraph_sdk import Auth
from starlette.authentication import AuthCredentials, BaseUser
from starlette.exceptions import HTTPException

T = TypeVar("T")
Row: TypeAlias = dict[str, Any]
AuthContext = contextvars.ContextVar[Auth.types.BaseAuthContext | None](
    "AuthContext", default=None
)


@asynccontextmanager
async def with_user(user: BaseUser | None = None, auth: AuthCredentials | None = None):
    current = get_auth_ctx()
    set_auth_ctx(user, auth)
    yield
    if current is None:
        return
    set_auth_ctx(current.user, AuthCredentials(scopes=current.scopes))


def set_auth_ctx(user: BaseUser | None, auth: AuthCredentials | None) -> None:
    if not user or not auth:
        AuthContext.set(None)
    else:
        AuthContext.set(
            Auth.types.BaseAuthContext(
                scopes=auth.scopes,
                user=user,
            )
        )


def get_auth_ctx() -> Auth.types.BaseAuthContext | None:
    return AuthContext.get()


class AsyncCursorProto(Protocol):
    async def fetchone(self) -> Row: ...

    async def fetchall(self) -> list[Row]: ...

    async def __aiter__(self) -> AsyncIterator[Row]:
        yield ...


class AsyncPipelineProto(Protocol):
    async def sync(self) -> None: ...


class AsyncConnectionProto(Protocol):
    @asynccontextmanager
    async def pipeline(self) -> AsyncIterator[AsyncPipelineProto]:
        yield ...

    async def execute(self, query: str, *args, **kwargs) -> AsyncCursorProto: ...


async def fetchone(
    it: AsyncIterator[T],
    *,
    not_found_code: int = 404,
    not_found_detail: str | None = None,
) -> T:
    """Fetch the first row from an async iterator."""
    try:
        return await anext(it)
    except StopAsyncIteration:
        raise HTTPException(
            status_code=not_found_code, detail=not_found_detail
        ) from None


def validate_uuid(uuid_str: str, invalid_uuid_detail: str | None) -> uuid.UUID:
    try:
        return uuid.UUID(uuid_str)
    except ValueError:
        raise HTTPException(status_code=422, detail=invalid_uuid_detail) from None


def next_cron_date(schedule: str, base_time: datetime) -> datetime:
    import croniter

    cron_iter = croniter.croniter(schedule, base_time)
    return cron_iter.get_next(datetime)
