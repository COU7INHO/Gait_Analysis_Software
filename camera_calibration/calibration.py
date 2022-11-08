import numpy as np
import cv2
import glob
import yaml
import os

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:6,0:9].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

#images = glob.glob('**/*.jpg')
#images = glob.glob(os.path.join('./camera_calibration/', "*.jpg"))

all_files = os.listdir("/Users/tiagocoutinho/Desktop/Gait_Software/camera_calibration")
images = list(filter(lambda f: f.endswith('.jpg'), all_files))


found = 0
for fname in images:  # Here, 10 can be changed to whatever number you like to choose
    image_path = os.path.join('/Users/tiagocoutinho/Desktop/Gait_Software/camera_calibration',fname)
    img = cv2.imread(image_path) # Capture frame-by-frame
    img = cv2.resize(img, (1200, 720))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (6,9), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)   # Certainly, every loop objp is the same, in 3D.
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (6,9), corners2, ret)
        found += 1
        cv2.imshow('img', img)
        cv2.waitKey(0)


print("Number of images used for calibration: ", found)

# When everything done, release the capture
# cap.release()
cv2.destroyAllWindows()

# calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# transform the matrix and distortion coefficients to writable lists
data = {'camera_matrix': np.asarray(mtx).tolist(),
        'dist_coeff': np.asarray(dist).tolist()}

# and save it to a file
with open("calibration_matrix.yaml", "w") as f:
    yaml.dump(data, f)