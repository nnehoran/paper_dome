import numpy as np
import cv2

## Load an color image in grayscale
#img = cv2.imread('dog.jpg',0)

#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.rectangle(gray,(384,0),(510,128),(0,255,0),3)


    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


