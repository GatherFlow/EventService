
import asyncio
import fastapi
import uvicorn
from contextlib import asynccontextmanager

from .endpoint import event_router
from .updater import Updater
from .middlewares import CheckAuthMiddleware

from config import get_settings


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
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


def start_app():
    settings = get_settings()
    uvicorn.run(app, host=settings.app.host, port=settings.app.port)
