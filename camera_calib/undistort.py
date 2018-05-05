import cv2
import numpy as np
import imutils
import sys

# You should replace these 3 lines with the output in calibration step
DIM=(500,281)
K=np.array([[141.5397401710071, 0.0, 255.8631844697084],[0.0, 144.617891687703, 137.29230524346895],[0.0, 0.0, 1.0]])
D=np.array([[-0.01993071014935031],[-0.0378178318994621018],[0.016178318994621018],[-0.002888987111754639]])
def undistort(img_path):
    img = cv2.imread(img_path)
    img = imutils.resize(img, width=500)

    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)