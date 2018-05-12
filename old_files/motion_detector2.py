# import the necessary packages
import datetime
import imutils
import time
import cv2
import numpy as np
 
camera = cv2.VideoCapture(1)
time.sleep(1)
(_, frame) = camera.read()

# initialize the first frame in the video stream
refFrame = None
refFramInit = [False, False, False]

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
    
    mask = np.zeros_like(gray)

    for c in range(3):
        channel = frame[:,:,c]
        blurred_channel = cv2.GaussianBlur(channel, (5, 5), 0)

        # if the first frame is None, initialize it
        if not refFramInit[c]:
            # if the first frame is None, initialize it
            if refFrame is None:
                refFrame = np.zeros_like(frame)

            refFrame[:,:,c] = blurred_channel
            refFramInit[c] = True
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(refFrame[:,:,c], blurred_channel)
        channel_mask = cv2.threshold(frameDelta, 25, 1, cv2.THRESH_BINARY)[1]
        mask = np.logical_or(mask, channel_mask)
 
    masked_gray = mask*gray

    threshold = 0.7*np.max(masked_gray)
    thresh = cv2.threshold(masked_gray, threshold, 255, cv2.THRESH_BINARY)[1]

    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
 
    max_area = 0
    max_area_index = -1
    # find the largest contour
    for i in range(len(cnts)):
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
    cv2.imshow("Security Feed", frame)
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