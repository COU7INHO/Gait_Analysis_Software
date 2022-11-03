import cv2

camera = cv2.VideoCapture(1)
tracker = cv2.legacy.TrackerKCF_create()
success, frame = camera.read()
bbox = cv2.selectROI("Tracking", frame, False )
tracker.init(frame, bbox)

def drawbox(frame, bbox):
    x, y, width, height = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 255), 3, 1)
    cv2.putText(frame, "Tracking", (75, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)


while True:
    timer = cv2.getTickCount()
    success, frame = camera.read()

    success, bbox = tracker.update(frame)

    if success:
        drawbox(frame, bbox)
    else:
        cv2.putText(frame, "Lost", (75, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)


    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
    