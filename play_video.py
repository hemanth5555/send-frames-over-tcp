#!/usr/bin/env python3
import cv2 as cv

cap = cv.VideoCapture("surf.mp4")

frames = list()

while cap.isOpened():
    ret, frame = cap.read()
    frames.append(frame)
    
    # if frame is read correctly, ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # make the fram gray and display it
    cv.imshow("frame", gray)

    # time to wait in ms
    if cv.waitKey(10) == ord("q"):
        print("you pressed 'q' and we will exit")
        break

cap.release()
# cv.destroyAllWindows()

for frame in frames:
    cv.imshow("frame", frame)
    if cv.waitKey(40) == ord("q"):
        print("you pressed 'q' and we will exit")
        break

cv.destroyAllWindows()

