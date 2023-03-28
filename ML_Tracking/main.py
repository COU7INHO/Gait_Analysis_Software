import cv2
from motionAnalysis_class import MotionAnalysis

#obj = MotionAnalysis("/Users/tiagocoutinho/Desktop/video3.mov", "Motion Analysis")
obj = MotionAnalysis(0, "Motion Analysis")

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
