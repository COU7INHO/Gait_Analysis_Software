import cv2
import os

class CalibrationImages:

    def __init__(self, camera_indices):
        self.camera_indices = camera_indices
        self.cameras = []
        self.paths = []
        self.camera_index = []
        for camera_index in self.camera_indices:
            self.camera_index.append(camera_index)
            self.cameras.append(cv2.VideoCapture(camera_index))
            path = f"./vision_calibration/images_to_calibrate/Camera{camera_index}/"  #! Path format for MacOS
            if not os.path.exists(path):
                os.makedirs(path)
            self.paths.append(path)
                
    def get_images(self):
        i = 0
        for camera in self.cameras:
            n_images = 0

            while camera.isOpened():
                _, img = camera.read()
                k = cv2.waitKey(5)

                if k == 27:
                    print(f"There are {n_images} images to calibrate Camera{self.camera_index[i]}")
                    break

                elif k == ord('s'): 
                    
                    cv2.imwrite(self.paths[self.camera_index[i]] + "Cam" + str(self.camera_index[i]) + '_' + str(n_images) + '.jpg', img)
                    print("Image saved!")
                    n_images += 1

                cv2.imshow('Img',img)
            i += 1

            camera.release()
            cv2.destroyAllWindows()

cameras = CalibrationImages([0, 1])
cameras.get_images()