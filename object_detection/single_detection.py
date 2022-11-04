import numpy as np
import cv2

img = cv2.imread("/Users/tiagocoutinho/Desktop/body.png")
template = cv2.imread("/Users/tiagocoutinho/Desktop/marker.png")

result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

threshold = 0.8
if max_val >= threshold:
    template_w = template.shape[0]
    template_h = template.shape[1]

    top_left = max_loc
    bottom_right = (top_left[0] + template_w, top_left[1] + template_h)

    cv2.rectangle(img, top_left, bottom_right,color=(0, 0, 255), thickness=2, lineType=cv2.LINE_4)

    cv2.imshow('Final Image.png', img)
    cv2.waitKey(0)

else:
    print("Error")