import cv2
from video.capture_video import VideoCapture
from video.show_window import DisplayFrames

cameras = VideoCapture([0, 1])
display = DisplayFrames(cameras)

while True:

    display.show()

    if cv2.waitKey(1) == ord('q'):
        break

cameras.release()
cv2.destroyAllWindows()