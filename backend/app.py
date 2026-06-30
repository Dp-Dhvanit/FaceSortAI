from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import os
import tempfile

from ai.detect_faces import detect_faces
from ai.sorter import sort_image

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


@app.post("/upload")
async def upload_images(files: list[UploadFile] = File(...)):

    with_faces = 0
    without_faces = 0

    for file in files:

        # Read uploaded image
        image_bytes = await file.read()

        # Save temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_file.write(image_bytes)
        temp_file.close()

        temp_path = temp_file.name

        # Convert bytes to OpenCV image
        np_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        
        has_face = detect_faces(image)

        # Sort image
        if has_face:
            with_faces += 1
            sort_image(temp_path, True)
        else:
            without_faces += 1
            sort_image(temp_path, False)

        # Delete temporary file
        os.remove(temp_path)

    return {
        "total": len(files),
        "with_faces": with_faces,
        "without_faces": without_faces
    }