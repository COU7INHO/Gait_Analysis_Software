import cv2
from start_recording.capture_video import VideoCapture
from start_recording.show_window import DisplayFrames

cameras = VideoCapture([0])
display = DisplayFrames(cameras)

while True:

    display.show()

    if cv2.waitKey(1) == ord('q'):
        break

cameras.release()
cv2.destroyAllWindows()