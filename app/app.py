
import fastapi
import uvicorn
from .hello import hello_router


app = fastapi.FastAPI()
app.include_router(hello_router)


def start_app():
    uvicorn.run(app, host="0.0.0.0", port=8000)
