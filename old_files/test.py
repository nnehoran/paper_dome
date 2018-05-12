import numpy as np
import cv2
import imutils
import time

SENSITIVITY = 10
BLUR_SIZE = 11

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'));
camera.set(cv2.CAP_PROP_FRAME_WIDTH,1920);
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,1080);
# camera.set(cv2.CAP_PROP_FPS,60);

# time.sleep(1)
# (_, frame) = camera.read()

prev_gray = None
# frame_count = 0
while(True):
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
 
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        print('frame could not be read')
        break
 
    # print(frame.shape)

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, height=720)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (BLUR_SIZE, BLUR_SIZE), 0)
 
    # if the first frame is None, initialize it
    if prev_gray is None:
        prev_gray = gray
        continue

    # Find the difference between this frame and the last
    diff = cv2.absdiff(gray, prev_gray)

    # Threshold the differences
    (_, thresh_diff) = cv2.threshold(diff, SENSITIVITY, 255, cv2.THRESH_BINARY)

    thresh_diff = cv2.GaussianBlur(thresh_diff, (BLUR_SIZE, BLUR_SIZE), 0)
    (_, thresh_diff) = cv2.threshold(thresh_diff, SENSITIVITY, 255, cv2.THRESH_BINARY)

    # Find the largest contour
    (_, cnts, _) = cv2.findContours(thresh_diff.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) >= 1:
        # compute the bounding box for the contour, draw it on the frame
        (x, y, w, h) = cv2.boundingRect(cnts[-1])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # frame_count = frame_count + 1
    # if frame_count >= 60:
    prev_gray = gray
    #     frame_count = 0

    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('thresh_diff', thresh_diff)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()


