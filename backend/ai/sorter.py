import os
import shutil

# Base processed folder
PROCESSED_DIR = "processed"

PEOPLE_DIR = os.path.join(PROCESSED_DIR, "People")
NO_PEOPLE_DIR = os.path.join(PROCESSED_DIR, "NoPeople")


def create_output_folders():
    """
    Create output folders if they don't exist.
    """

    os.makedirs(PEOPLE_DIR, exist_ok=True)
    os.makedirs(NO_PEOPLE_DIR, exist_ok=True)


def clear_output_folders():
    """
    Remove previous scan results.
    """

    create_output_folders()

    for folder in [PEOPLE_DIR, NO_PEOPLE_DIR]:

        for file in os.listdir(folder):

            file_path = os.path.join(folder, file)

            if os.path.isfile(file_path):
                os.remove(file_path)


def sort_image(source_path, has_face):
    """
    Copy image into the correct output folder.
    """

    create_output_folders()

    filename = os.path.basename(source_path)

    if has_face:
        destination = os.path.join(PEOPLE_DIR, filename)
    else:
        destination = os.path.join(NO_PEOPLE_DIR, filename)

    shutil.copy2(source_path, destination)