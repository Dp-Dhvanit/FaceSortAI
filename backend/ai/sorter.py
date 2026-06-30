import os
import shutil

WITH_FACES = "processed/with_faces"
WITHOUT_FACES = "processed/without_faces"

os.makedirs(WITH_FACES, exist_ok=True)
os.makedirs(WITHOUT_FACES, exist_ok=True)

def sort_image(source_path, has_face):
    filename = os.path.basename(source_path)

    if has_face:
        destination = os.path.join(WITH_FACES, filename)
    else:
        destination = os.path.join(WITHOUT_FACES, filename)

    shutil.copy2(source_path, destination)