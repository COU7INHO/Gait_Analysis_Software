import cv2 as cv
from Single_Camera_Calibration.CameraCalibration import CalibrateCamera


class DisplayVideo(CalibrateCamera):

    def __init__(self, cam1_index, cam2_index):
        super().__init__(cam1_index, cam2_index)
        
    def display(self):
        
        for index, camera in zip(self.indices, self.cameras):
            cv_file = cv.FileStorage()
            cv_file.open(f"./Single_Camera_Calibration/map{index}.xml", cv.FileStorage_READ)

            map_x = cv_file.getNode(f"map{index}_x").mat()
            map_y = cv_file.getNode(f"map{index}_y").mat()

            while camera.isOpened():
                success, frame = camera.read()
                frame = cv.remap(frame, map_x, map_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
                cv.imshow(f"Calibrated video, Camera{index}", frame)
                if cv.waitKey(1) == ord('q'):
                    break

            camera.release()
            cv.destroyAllWindows()   