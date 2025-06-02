from http.client import responses

import aiohttp
from loguru import logger

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from config import get_settings


class CheckAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        BaseHTTPMiddleware.__init__(self, app)

        self.log = logger.bind(classname=self.__class__.__name__)
        self.user_service_endpoint = get_settings().services.user
        if self.user_service_endpoint.endswith("/"):
            self.user_service_endpoint = self.user_service_endpoint[:-1]

    async def get_user_id(self, cookies: dict) -> str | None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=f"{self.user_service_endpoint}/me",
                    cookies=cookies,
                    raise_for_status=True
                ) as response:
                    self.log.debug(f"{response} -> {await response.text()}")

                    data = await response.json()
                    return data["id"]

        except Exception as err:
            return None

    async def dispatch(self, request: Request, call_next):
        dest = str(request.url).split("/")[-1]
        if dest in ["docs", "openapi.json"]:
            response = await call_next(request)
            return response

        key = request.cookies.get("api_key")
        if key == get_settings().app.key:
            user_id = request.cookies.get("user_id")

        else:
            user_id = await self.get_user_id(request.cookies)

            if not user_id:
                return JSONResponse(
                    status_code=401,
                    content={"detail": f"You are not allowed to access this endpoint"}
                )

        request.state.user_id = user_id

        response = await call_next(request)
        return response
