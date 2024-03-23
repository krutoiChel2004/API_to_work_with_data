from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse

from src.video.service import cutting_video_into_frames_service


router = APIRouter(prefix="/video",
                    tags=["video"],)


@router.post("/cutting_video_into_frames")
async def cutting_video_into_frames(video: UploadFile):
    
    await cutting_video_into_frames_service(video)

@router.get("/get_zip_with_frames")
async def get_zip_with_frames():
    return FileResponse(path='src/video/zip/frames.zip', filename='frames.zip', media_type='multipart/form-data')