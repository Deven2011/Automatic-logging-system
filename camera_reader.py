import cv2

def get_camera_stream(source):
    """
    source can be:
    - RTSP URL
    - video file path
    - image path
    """
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        raise RuntimeError("❌ Cannot open camera source")

    return cap
