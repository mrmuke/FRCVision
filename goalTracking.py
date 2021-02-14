from imutils.video import VideoStream
import cv2
import imutils
import numpy as np
vs = VideoStream(src=0).start()

while True:
    frame = vs.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if(len(cnts) > 0):
        c = max(cnts, key=cv2.contourArea)
        marker=cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
        box = np.int0(box)
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

    if(mask[240][320] > 0):
        print("green")

    cv2.imshow("Goal Tracking", frame)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

vs.stop()
cv2.destroyAllWindows()