import numpy as np
import cv2
import imutils
import time
import glob
import math

class Camera:
    """docstring for Camera"""
    def __init__(self, _id, native_res = (1080, 1920), crop_bounds = None,
        scale_to_height = 500):

        self._id = _id
        self.native_width = native_res[1]
        self.native_height = native_res[0]
        self.crop_bounds = crop_bounds
        self.scale_to_height = scale_to_height
        self.cam = None
        self.K = None
        self.D = None

    def set_native_res(self, width, height):
        self.native_width = width
        self.native_height = height
        if not self.cam is None and self.cam.isOpened():
            return self.start_capture()
        return True

    def set_scale_to_height(self, height):
        self.scale_to_height = height
        return True
        
    def set_crop_bounds(self, bounds):
        self.crop_bounds = bounds

    def start_capture(self):
        if self.cam is None:
            self.cam = cv2.VideoCapture(self._id)
        if self.cam.isOpened():
            self.cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'));
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.native_height);
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.native_width);

            img = self.capture_img()
            if not img is None:
                print('capture started at resolution %s' %str(img.shape[:2]))
                return True
            else:
                print('could not capture a frame')
        else:
            print('could not open the camera')

        return False

    def stop_capture(self):
        if not self.cam is None:
            self.cam.release()
            print('capture stopped')
            return True
        return False

    def capture_img(self):
        if self.cam is None:
            print('camera has not been opened')
            return None

        (captured, img) = self.cam.read()
        if not captured:
            print('could not capture a frame')
            return None

        if not self.crop_bounds is None:
            img = img[self.crop_bounds[0]:self.crop_bounds[1],
                self.crop_bounds[2]:self.crop_bounds[3]]

        return imutils.resize(img, height=self.scale_to_height)

    def get_rectilinear(self, scale = 1):
        fisheye = self.capture_img()
        k_new = self.K.copy()
        k_new[0,0] = k_new[0,0]/scale
        k_new[1,1] = k_new[1,1]/scale
        return cv2.fisheye.undistortImage(fisheye, self.K, self.D, Knew = k_new)

    def get_equirectangular(self, theta_range = 180, phi_range = 90):
        fisheye = self.capture_img()
        fisheye_width = np.shape(fisheye)[1]
        fisheye_height = np.shape(fisheye)[0]

        # recti = self.get_rectilinear()
        # recti_width = np.shape(recti)[1]
        # recti_height = np.shape(recti)[0]

        res_height = self.scale_to_height
        res_width = int(self.scale_to_height/phi_range*theta_range)
        result = np.zeros((res_height, res_width, 3), np.uint8)

        for y in range(res_height):
            for x in range(res_width):
                phi = (y/res_height - 0.5)*phi_range*math.pi/180
                theta = (x/res_width - 0.5)*theta_range*math.pi/180

                recti_pt = np.zeros((1, 1, 2))
                recti_pt[0,0,0] = self.K[0,0]*math.tan(theta) + self.K[0,2]
                recti_pt[0,0,1] = self.K[1,1]*math.tan(phi) + self.K[1,2]

                # recti_x = int(recti_pt[0,0,0])
                # recti_y = int(recti_pt[0,0,1])
                # # print('%s, %s' %(recti_x, recti_y))
                # if not (recti_x < 0 or recti_x >= recti_width) and \
                #     not (recti_y < 0 or recti_y >= recti_height):
                #     result[y,x,:] = recti[recti_y,recti_x,:]
                #     # print(recti[recti_y,recti_x,:])

                P = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(self.K, self.D, (fisheye_height,fisheye_width), np.array([]))
                recti_pt[0,0,:] = np.matmul(np.linalg.inv(P),np.array([recti_pt[0,0,0],recti_pt[0,0,1],1]))[0:2]

                fisheye_pt = cv2.fisheye.distortPoints(recti_pt, self.K, self.D)
                fisheye_x = int(fisheye_pt[0,0,0])
                fisheye_y = int(fisheye_pt[0,0,1])
                # print('%s, %s' %(fisheye_x, fisheye_y))

                if not (fisheye_x < 0 or fisheye_x >= fisheye_width) and \
                    not (fisheye_y < 0 or fisheye_y >= fisheye_height):
                    result[y,x,:] = fisheye[fisheye_y,fisheye_x,:]

        return result

    def calibrate(self, img_path = '', checkerboard_dims = (6,9)):
        subpix_criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
        calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_CHECK_COND+cv2.fisheye.CALIB_FIX_SKEW
        objp = np.zeros((1, checkerboard_dims[0]*checkerboard_dims[1], 3), np.float32)
        objp[0,:,:2] = np.mgrid[0:checkerboard_dims[0], 0:checkerboard_dims[1]].T.reshape(-1, 2)
        _img_shape = None
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        images = glob.glob('%s*.jpg' %img_path)
        for fname in images:
            img = cv2.imread(fname)
            if not self.crop_bounds is None:
               img = img[self.crop_bounds[0]:self.crop_bounds[1],
                    self.crop_bounds[2]:self.crop_bounds[3]]
            img = imutils.resize(img, height=self.scale_to_height)

            if _img_shape == None:
                _img_shape = img.shape[:2]
            else:
                assert _img_shape == img.shape[:2], "All images must share the same size."
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, checkerboard_dims, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                cv2.cornerSubPix(gray,corners,(3,3),(-1,-1),subpix_criteria)
                imgpoints.append(corners)
        N_OK = len(objpoints)
        K = np.zeros((3, 3))
        D = np.zeros((4, 1))
        rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
        tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
        rms, _, _, _, _ = \
            cv2.fisheye.calibrate(
                objpoints,
                imgpoints,
                gray.shape[::-1],
                K,
                D,
                rvecs,
                tvecs,
                calibration_flags,
                (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
            )

        self.K = K
        self.D = D

        print("Found " + str(N_OK) + " valid images for calibration")
        print("DIM=" + str(_img_shape[::-1]))
        print("K=np.array(" + str(K.tolist()) + ")")
        print("D=np.array(" + str(D.tolist()) + ")")

    def calculate_equi_mapping():
        pass