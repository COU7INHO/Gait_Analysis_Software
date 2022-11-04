import cv2 as cv
import numpy as np


img_rgb = cv.imread("/Users/tiagocoutinho/Desktop/body.png")
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread("/Users/tiagocoutinho/Desktop/marker.png",0)
w, h = template.shape[::-1]

result = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.8
location = np.where( result >= threshold)

for location in zip(*location[::-1]):
    cv.rectangle(img_rgb, location, (location[0] + w, location[1] + h), (0,0,255), 1)

cv.imshow('Imagem.png',img_rgb)

cv.waitKey(0)