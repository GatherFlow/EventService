
import fastapi
import os

from fastapi.responses import FileResponse


images_router = fastapi.APIRouter(prefix="/image")


@images_router.get(
    path="/{album_id}",
    response_class=FileResponse,
    description="Get image"
)
async def create_event(
    album_id: str,
):

    file_path = f"./resources/images/{album_id}"
    if not os.path.isdir(file_path):
        file_path = f"./resources/images/404.jpg"

    return FileResponse(path=file_path, media_type="image/jpeg", filename=f"image.jpg")
