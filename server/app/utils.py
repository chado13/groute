
from collections.abc import Awaitable, Callable

from functools import wraps
from typing import Any


from fastapi import Response
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from starlette.status import HTTP_200_OK


def fast_response(
    *, status_code: int = HTTP_200_OK
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[ORJSONResponse | Response]]]:
    def decorator(
        func: Callable[..., Awaitable[Any]],
    ) -> Callable[..., Awaitable[ORJSONResponse | Response]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> ORJSONResponse | Response:
            response = await func(*args, **kwargs)

            if isinstance(response, BaseModel):
                return Response(
                    content=response.model_dump_json(),
                    media_type="application/json",
                    status_code=status_code,
                )
            else:
                return ORJSONResponse(response, status_code=status_code)

        return wrapper

    return decorator