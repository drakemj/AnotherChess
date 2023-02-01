import cv2
import numpy as np

# Load the image
img = cv2.imread("test.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Use image thresholding to isolate the chess pieces
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Find contours in the thresholded image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Loop through each contour and classify it as a chess piece
for cnt in contours:
    # Calculate the area of the contour
    area = cv2.contourArea(cnt)

    # Skip small contours that are likely not chess pieces
    if area < 100:
        continue

    # Calculate the aspect ratio of the contour
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = float(w) / h

    # Classify the contour as a pawn if its aspect ratio is close to 1
    if 0.8 < aspect_ratio < 1.2:
        cv2.drawContours(img, [cnt], 0, (0, 0, 255), 2)
        cv2.putText(img, "Pawn", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    # Classify the contour as a rook if its aspect ratio is much greater than 1
    elif aspect_ratio > 1.5:
        cv2.drawContours(img, [cnt], 0, (0, 255, 0), 2)
        cv2.putText(img, "Rook", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    # Classify the contour as a bishop if its aspect ratio is much less than 1
    elif aspect_ratio < 0.7:
        cv2.drawContours(img, [cnt], 0, (255, 0, 0), 2)
        cv2.putText(img, "Bishop", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    # Classify the contour as a queen if its area is large
    elif area > 1000:
        cv2.drawContours(img, [cnt], 0, (255, 255, 0), 2)
        cv2.putText(img, "Queen", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        # Classify the contour as a king if its area is larger than the other pieces
    elif area > 1500:
        cv2.drawContours(img, [cnt], 0, (0, 255, 255), 2)
        cv2.putText(img, "King", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    # Classify the contour as a knight if its aspect ratio is around 0.5
    elif 0.4 < aspect_ratio < 0.6:
        cv2.drawContours(img, [cnt], 0, (255, 0, 255), 2)
        cv2.putText(img, "Knight", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Show the image with the chess pieces labeled
cv2.imshow("Chess Pieces", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
