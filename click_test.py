import numpy as np
import cv2
import glob
import math
import Camera
import maestro
import time

MIN_PULSE = 496*4
MAX_PULSE= 2448*4
CENTER_PULSE = (MAX_PULSE + MIN_PULSE)/2
PULSE_RANGE = MAX_PULSE - MIN_PULSE
ANGLE_RANGE = 170

def set_target(yaw, pitch):
    target_pulse = int(CENTER_PULSE - yaw*PULSE_RANGE/ANGLE_RANGE)
    # target_pulse = min(target_pulse, MAX_PULSE)
    # target_pulse = max(target_pulse, MIN_PULSE)
    if target_pulse >= MIN_PULSE and target_pulse <= MAX_PULSE:
        servo_con.setSpeed(0,0)
        servo_con.setTarget(0,target_pulse)


def handle_click(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pts = np.zeros((1, 1, 2))
        pts[0,0,0] = x
        pts[0,0,1] = y
        result = cv2.fisheye.undistortPoints(pts, cam.K, cam.D, P=cam.K)
        yaw = math.floor(math.atan2(result[0,0,0] - cam.K[0,2], cam.K[0,0])*1800/math.pi)/10.0
        pitch = math.floor(math.atan2(-result[0,0,1] + cam.K[1,2], cam.K[1,1])*1800/math.pi)/10.0
        # print('x:%s, y:%s' %(str(x),str(y)))
        print('yaw: %s, pitch: %s' %(str(yaw),str(pitch)))

        # set_target(yaw, pitch)

# servo_con = maestro.Controller('COM3')

cam = Camera.Camera(_id = 1, crop_bounds = (0, 1080, 210, 1760), scale_to_height = 720)
cam.calibrate(img_path = 'C:/Nadav/Repos/paper_dome/camera_calib/')
cam.start_capture()

cv2.namedWindow('image')
cv2.setMouseCallback('image', handle_click)
while True:
    img = cam.capture_img()
    # img = cam.get_rectilinear(3)
    # img = cam.get_equirectangular()
    if img is None:
        print('frame could not be read')
        break
    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cam.stop_capture()
cv2.destroyAllWindows()
