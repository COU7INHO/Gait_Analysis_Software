import cv2

def calibrated_images(cam_index1, cam_index2):
    cv_file = cv2.FileStorage()
    cv_file.open("./vision_calibration/stereoMap.xml", cv2.FileStorage_READ)

    stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
    stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
    stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
    stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

    cam1 = cv2.VideoCapture(cam_index1)                    
    cam2 =  cv2.VideoCapture(cam_index2)

    while(cam1.isOpened() and cam2.isOpened()):

        _, img1 = cam1.read()
        _, img2 = cam2.read()

        img1 = cv2.remap(img1, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        img2 = cv2.remap(img2, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                        
        cv2.imshow("Camera 1 calibrated", img1) 
        cv2.imshow("Camera 2 calibrated", img2)

        if cv2.waitKey(1) == ord('q'):
            break

    cam1.release()
    cam2.release()

    cv2.destroyAllWindows()