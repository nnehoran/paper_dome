import Camera
import Gun
import cv2
import numpy as np
import math

class Tracker:
    """docstring for Tracker"""

    BLUR_SIZE = 11
    SENSITIVITY = 10
    MIN_OBJECT_AREA = 500

    def __init__(self, cam_id = 1):
        self.gun = Gun.Gun()
        self.camera = Camera.Camera(_id = cam_id, crop_bounds = (200, 1080, 210, 1760), scale_to_height = 500)
        self.camera.calibrate(img_path = 'C:/Nadav/Repos/paper_dome/camera_calib/')

    def track_object(self, old_frame, new_frame):
        # Find the difference between this frame and the last
        diff = cv2.absdiff(new_frame, old_frame)

        # Threshold the differences
        (_, thresh_diff) = cv2.threshold(diff, self.SENSITIVITY, 255, cv2.THRESH_BINARY)

        thresh_diff = cv2.GaussianBlur(thresh_diff, (self.BLUR_SIZE, self.BLUR_SIZE), 0)
        (_, thresh_diff) = cv2.threshold(thresh_diff, self.SENSITIVITY, 255, cv2.THRESH_BINARY)

        # Find the largest contour
        (_, cnts, _) = cv2.findContours(thresh_diff.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) >= 1:
            # compute the bounding box for the contour, draw it on the frame
            return  cv2.boundingRect(cnts[-1])
        else:
            return (None, None, None, None)

    def calc_angle(self, x, y):
        pts = np.zeros((1, 1, 2))
        pts[0,0,0] = x
        pts[0,0,1] = y
        result = cv2.fisheye.undistortPoints(pts, self.camera.K, self.camera.D, P=self.camera.K)
        yaw = math.floor(math.atan2(result[0,0,0] - self.camera.K[0,2], self.camera.K[0,0])*1800/math.pi)/10.0
        pitch = math.floor(math.atan2(-result[0,0,1] + self.camera.K[1,2], self.camera.K[1,1])*1800/math.pi)/10.0
        # print('x:%s, y:%s' %(str(x),str(y)))
        print('yaw: %s, pitch: %s' %(str(yaw),str(pitch)))
        return (yaw, pitch)

    def main(self):
        self.camera.start_capture()

        prev_gray = None
        while True:
            frame = self.camera.capture_img()
            # img = self.camera.get_rectilinear(1)
            # img = self.camera.get_equirectangular()
            if frame is None:
                print('frame could not be read')
                break

            # convert the frame to grayscale, and blur it
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (self.BLUR_SIZE, self.BLUR_SIZE), 0)
         
            # if the first frame is None, initialize it
            if prev_gray is None:
                prev_gray = gray
                continue

            (x, y, w, h) = self.track_object(prev_gray, gray)

            if x is not None:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                mid_x = x + w//2
                mid_y = y + h//2

                (yaw, pitch) = self.calc_angle(x, y)

                self.gun.set_yaw(yaw, speed = 20)
                self.gun.set_pitch(pitch, speed = 15)
                if w*h >= self.MIN_OBJECT_AREA:
                    self.gun.fire()
                else:
                    self.gun.stop_fire()

            prev_gray = gray

            # Display the resulting frame
            cv2.imshow('frame', frame)
            # cv2.imshow('thresh_diff', thresh_diff)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.camera.stop_capture()
        self.gun.go_to_zero(20)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = Tracker()
    tracker.main()