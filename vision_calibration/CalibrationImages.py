import cv2

#? https://www.youtube.com/watch?v=yKypaVl6qQo


class CalibrateImages:

    def __init__(self, camera_index:int, camera_name:str, path:str, image_name:str):
        self.camera_index = camera_index
        self.camera_name = camera_name
        self.path = path
        self.image_name = image_name
        
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
                cv2.imwrite(self.path + self.image_name + str(n_images) + '.jpg', img)
                print("Image saved!")
                n_images += 1

            cv2.imshow('Img',img)

        camera.release()
        cv2.destroyAllWindows()
        
        return success, img

camL = CalibrateImages(0, "webcam", "./vision_calibration/images_to_calibrate/imageL/", "imgL_" )
camR = CalibrateImages(1, "iphone", "./vision_calibration/images_to_calibrate/imageR/", "imgR_" )

camL.get_images()
camR.get_images()