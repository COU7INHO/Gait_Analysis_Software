import cv2
from motionAnalysis_class import MotionAnalysis


obj = MotionAnalysis("/Users/tiagocoutinho/Desktop/videos/ciclo.mov", "Motion Analysis")

obj.openCamera()
obj.timeInit()
obj.getFrame()
obj.trackerInit()      

while True:
    obj.getFrame()
    obj.removeEmptyBoxes()
    obj.checkMarkers()
    obj.getCenters()  
    obj.getDirection()
    obj.calcAngles()
    obj.px_to_cm(20)
    obj.lines()
    obj.labels()
    obj.timeStop()
    obj.displayWindow()

    if cv2.waitKey(1) == ord('q'):
        break

obj.closeWindow()
cv2.destroyAllWindows()
