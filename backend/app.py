from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import cv2
import numpy as np
import os
import tempfile
import time
import zipfile

from concurrent.futures import ThreadPoolExecutor

from ai.detect_faces import detect_faces
from ai.sorter import (
    sort_image,
    clear_output_folders
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FaceSortAI Backend Running"}


def process_image(image_bytes):
    """
    Process one image.
    Returns True if a face is detected.
    """

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp_file.write(image_bytes)
    temp_file.close()

    temp_path = temp_file.name

    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    has_face = detect_faces(image)

    sort_image(temp_path, has_face)

    os.remove(temp_path)

    return has_face


@app.post("/upload")
async def upload_images(files: list[UploadFile] = File(...)):

    clear_output_folders()

    start_time = time.time()

    images = []

    for file in files:
        images.append(await file.read())

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_image, images))

    with_faces = sum(results)
    without_faces = len(results) - with_faces

    end_time = time.time()

    return {
        "status": "completed",
        "total": len(files),
        "with_faces": with_faces,
        "without_faces": without_faces,
        "scan_time": round(end_time - start_time, 2)
    }


@app.get("/download")
def download_results():

    zip_path = "processed/FaceSortAI_Results.zip"

    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:

        for folder_name in ["People", "NoPeople"]:

            folder_path = os.path.join("processed", folder_name)

            if not os.path.exists(folder_path):
                continue

            for root, dirs, files in os.walk(folder_path):

                for file in files:

                    file_path = os.path.join(root, file)

                    arcname = os.path.relpath(file_path, "processed")

                    zipf.write(file_path, arcname)

    return FileResponse(
        path=zip_path,
        filename="FaceSortAI_Results.zip",
        media_type="application/zip"
    )