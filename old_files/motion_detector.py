# import the necessary packages
import datetime
import imutils
import time
import cv2
import numpy as np
 
camera = cv2.VideoCapture(1)
time.sleep(1)
camera.read()

# initialize the first frame in the video stream
refFrame = None

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
 
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break
 
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
    # if the first frame is None, initialize it
    if refFrame is None:
        refFrame = gray
        continue
    # else:
    #     refFrame = refFrame*0.999 + gray*0.001

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(np.uint8(refFrame), gray)
    mask = cv2.threshold(frameDelta, 25, 1, cv2.THRESH_BINARY)[1]
 
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    # mask = cv2.dilate(mask, None, iterations=2)

    masked_gray = mask*gray

    threshold = 0.9*np.max(masked_gray)
    thresh = cv2.threshold(masked_gray, threshold, 255, cv2.THRESH_BINARY)[1]

    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
 
    max_area = 0
    max_area_index = -1
    # loop over the contours
    for i in range(len(cnts)):
        # if the contour is too small, ignore it
        area = cv2.contourArea(cnts[i])
        if area > max_area:
            max_area = area
            max_area_index = i

    if max_area_index > -1:
        cv2.drawContours(gray, cnts, max_area_index, 255, -1)
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(cnts[max_area_index])
        cv2.rectangle(gray, (x, y), (x + w, y + h), 0, 2)

    # show the frame and record if the user presses a key
    # cv2.imshow("Security Feed", frame)
    cv2.imshow("Masked Gray", masked_gray)
    # cv2.imshow("Frame Delta", frameDelta)
    cv2.imshow("gray", gray)
    key = cv2.waitKey(1) & 0xFF
 
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()