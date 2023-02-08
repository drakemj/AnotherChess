import cv2
import numpy as np

def detect_pieces(image1, image2):
    # Load the chessboard image
    image1 = cv2.imread(image1)
    print("Image 1 read")
    image2 = cv2.imread(image2)
    print("Image 2 read")
    if image1 is None:
        print("Error: Could not load test1.jpg")

    if image2 is None:
        print("Error: Could not load test2.jpg")
    # Convert both images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Detect the chessboard corners in both images
    ret1, corners1 = cv2.findChessboardCorners(gray1, (8,8), None)
    if ret1 is None: 
        print("Error no corner in 1")
    ret2, corners2 = cv2.findChessboardCorners(gray2, (8,8), None)
    if ret2 is None: 
        print("Error no corner in 2")
    print("ret1:", ret1)
    print("ret2:", ret2)
    if not ret1 or not ret2:
        print("No chessboard corners were detected.")
        return []
    # If the chessboard corners are found in both images
    if ret1 and ret2:
        print("Ret 1 and Ret 2 read")
    # Refine the corner positions
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    corners1 = cv2.cornerSubPix(gray1, corners1, (11,11), (-1,-1), criteria)
    corners2 = cv2.cornerSubPix(gray2, corners2, (11,11), (-1,-1), criteria)
    # calculate objects distance
    #ret, R, t, mask = cv2.solvePnPRansac(obj_points, corners2, intrinsic, dist_coeffs)
    #projected_points, _ = cv2.projectPoints(obj_points, R, t, intrinsic, dist_coeffs)
    #return projected_points
# Draw the corners on both images
    cv2.drawChessboardCorners(image1, (8,8), corners1, ret1)
    cv2.drawChessboardCorners(image2, (8,8), corners2, ret2)

    # Calculate the size of each square on the chessboard
    square_size = np.int0(np.linalg.norm(corners1[0] - corners1[7]))

    # Loop over all the squares on the chessboard
    for r in range(8):
        for c in range(8):
            # Calculate the top-left and bottom-right corners of the square
            top_left1 = corners1[8*r+c].ravel()
            bottom_right1 = top_left1 + square_size
            top_left2 = corners2[8*r+c].ravel()
            bottom_right2 = top_left2 + square_size

            # Extract the patch from both images for the current square
            patch1 = gray1[top_left1[1]:bottom_right1[1], top_left1[0]:bottom_right1[0]]
            patch2 = gray2[top_left2[1]:bottom_right2[1], top_left2[0]:bottom_right2[0]]
            print(patch1.shape, patch2.shape)
            # Calculate the mean squared difference between the patches
            mse = np.mean((patch1 - patch2) ** 2)

            # If the mean squared difference is above a threshold, consider it a moved piece
            if mse > 20:
                print("A piece has been moved from square ({}, {})".format(r, c))
            else: print("No pieces have been moved")
if __name__ == "__main__":
# Call the function to detect the moved pieces
    print("test")
    detect_pieces("test1.jpg", "test2.jpg")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
