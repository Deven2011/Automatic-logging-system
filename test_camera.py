from camera_reader import get_camera_stream
import cv2

cap = get_camera_stream("test_images/truck.jpg")  # use image or video

ret, frame = cap.read()
if ret:
    cv2.imshow("Frame", frame)
    cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
