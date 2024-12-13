from typing import Callable

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..cache import cache
from ..conf import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = self.get_client_ip(request)
        key = f"ratelimit:{client_ip}"

        requests = cache.get(key, 0)

        if requests >= settings.RATE_LIMIT:
            return JSONResponse(
                {"detail": "Limite de requisições excedido. Tente novamente mais tarde."},
                status.HTTP_429_TOO_MANY_REQUESTS,
            )

        cache[key] = requests + 1

        response = await call_next(request)

        return response

    @staticmethod
    def get_client_ip(request: Request) -> str:
        x_forwarded_for = request.headers.get("x-forwarded-for")

        ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.client.host

        return ip
