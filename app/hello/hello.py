
import fastapi


hello_router = fastapi.APIRouter(prefix="/abc")


@hello_router.get("")
async def send_message():
    return "<h1>Hello EventService</h1>"
