'''This script is used to collect the images that will be used to create a 
machine learning model to detect a specific object'''

import cv2 as cv

camera = cv.VideoCapture(1)

n = 0
while camera.isOpened():

    _, frame = camera.read()
    
    if cv.waitKey(1) == ord('s'):
        cv.imwrite("/Users/tiagocoutinho/Desktop/novas_imagens/"+"img_"+str(n)+".jpg", frame)
        print(f"Image Saved -> {n}")
        n += 1
        
    if cv.waitKey(1) == ord('q'):
        break

    cv.imshow("iPhone camera", frame)

    
camera.release()
cv.destroyAllWindows()



