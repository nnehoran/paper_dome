import numpy as np
import cv2
import imutils
import time

# You should replace these 3 lines with the output in calibration step
DIM=(1920,1080)
K=np.array([[545.9418929701941, 0.0, 984.9742287822712],[0.0, 558.480533603349, 530.1779538885085],[0.0, 0.0, 1.0]])
D=np.array([[-0.037845428775054354],[-0.014360572367903926],[0.005092543725544212],[-0.0012604122779025007]])

camera = cv2.VideoCapture(1)

camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'));
camera.set(cv2.CAP_PROP_FRAME_WIDTH,1920);
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,1080);
# camera.set(cv2.CAP_PROP_FPS,60);

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

    # frame = cv2.fisheye.undistortImage(frame, K, D, Knew = K)

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, height=720)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()


