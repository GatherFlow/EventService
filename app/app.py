
import asyncio
import fastapi
import uvicorn
from contextlib import asynccontextmanager

from sqlalchemy import text

from .endpoint import (
    event_router, like_router
)
from .updater import Updater
from .middlewares import CheckAuthMiddleware

from app.database import get_async_session

from config import get_settings


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    async with get_async_session() as session:
        await session.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        await session.commit()

    updater = Updater()
    task = asyncio.create_task(updater.start())

    yield

    # to avoid killing task
    print(task)


app = fastapi.FastAPI(
    title="Swagger",
    root_path=get_settings().app.path,
    lifespan=lifespan
)
app.add_middleware(CheckAuthMiddleware)

app.include_router(event_router)
app.include_router(like_router)


def start_app():
    settings = get_settings()
    uvicorn.run(app, host=settings.app.host, port=settings.app.port)
