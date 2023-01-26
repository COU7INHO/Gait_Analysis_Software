import cv2
import multiprocessing
from main_class import MotionAnalysis


def motionAnalysis(obj):
    obj.openCamera()
    obj.timeInit()
    obj.getFrame()
    obj.trackerInit()

    while True:
        obj.getFrame()
        obj.removeEmptyBoxes()
        obj.checkMarkers()
        obj.getCenters()
        obj.calcAngles()
        obj.timeStop()
        obj.displayWindow()

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    obj.closeWindow()


if __name__ == '__main__':

    obj1 = MotionAnalysis(0, "Motion Analysis 1")

    p1 = multiprocessing.Process(target=motionAnalysis, args=(obj1, ))

    p1.start()

    p1.join()
