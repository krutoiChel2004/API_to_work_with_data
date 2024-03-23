from fastapi import UploadFile
from fastapi.responses import JSONResponse
import zipfile
import cv2
import os

def extract_frames(video_path, save_frames_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        frame_filename = f"{save_frames_path}/frame_{frame_count}.jpg"
        cv2.imwrite(frame_filename, frame)
    cap.release()

async def cutting_video_into_frames_service(video: UploadFile):
    try:
        video_path = f"src/video/uploaded_videos/{video.filename}"
        with open(video_path, "wb") as buffer:
            buffer.write(await video.read())

        save_frames_path = "src/video/frames"
        if not os.path.exists(save_frames_path):
            os.makedirs(save_frames_path)

        extract_frames(video_path, save_frames_path)

        zip_filename = "src/video/zip/frames.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for root, _, files in os.walk(save_frames_path):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), save_frames_path))

        return JSONResponse(content={"message": "Видео успешно загружено и нарезано на кадры"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)