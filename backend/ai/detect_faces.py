import cv2
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

MODEL_DIR = os.path.join(BASE_DIR, "models")

PROTO_PATH = os.path.join(MODEL_DIR, "deploy.prototxt")
MODEL_PATH = os.path.join(
    MODEL_DIR,
    "res10_300x300_ssd_iter_140000.caffemodel"
)

# Load the DNN model once
net = cv2.dnn.readNetFromCaffe(PROTO_PATH, MODEL_PATH)


def detect_faces(image):
    """
    Returns True if at least one face is detected.
    Returns False otherwise.
    """

    if image is None:
        return False

    h, w = image.shape[:2]

    # Resize very large images for faster processing
    max_width = 800

    if w > max_width:
        scale = max_width / w
        image = cv2.resize(
            image,
            (int(w * scale), int(h * scale))
        )
        h, w = image.shape[:2]

    blob = cv2.dnn.blobFromImage(
        image,
        1.0,
        (300, 300),
        (104.0, 177.0, 123.0)
    )

    net.setInput(blob)
    detections = net.forward()

    confidence_threshold = 0.60

    for i in range(detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > confidence_threshold:
            return True

    return False