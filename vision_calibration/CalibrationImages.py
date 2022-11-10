import cv2
import os

class CalibrationImages:

    def __init__(self, camera_index:int, camera_name:str):
        self.camera_index = camera_index
        self.camera_name = camera_name   
        self.path = (f"./vision_calibration/images_to_calibrate/{self.camera_name}/" )  #! Path format for MMacOS   
        if not os.path.exists(self.path):
              self.path = os.makedirs(f"./vision_calibration/images_to_calibrate/{self.camera_name}/")

    def get_images(self):

        camera = cv2.VideoCapture(self.camera_index)

        n_images = 0

        while camera.isOpened():

            success, img = camera.read()
            k = cv2.waitKey(5)

            if k == 27:
                print(f"There are {n_images} to calibrate {self.camera_name}")
                break

            elif k == ord('s'): 
                cv2.imwrite(self.path + self.camera_name + str(n_images) + '.jpg', img)
                print("Image saved!")
                n_images += 1

            cv2.imshow('Img',img)

        camera.release()
        cv2.destroyAllWindows()
        
        return success, img

mac_webcam = CalibrationImages(0, "mac_webcam" )
iphone = CalibrationImages(1, "iphone_cam")
mac_webcam.get_images()
iphone.get_images()