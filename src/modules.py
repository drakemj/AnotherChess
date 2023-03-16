import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import math


def getBlob(img):
    img = cv.GaussianBlur(img, (5, 5), 0)
    edges = cv.Canny(img, 50, 50)

    kernel = np.ones((4, 4), np.uint8)
    dilation = cv.dilate(edges, kernel, iterations=1)
    ret, thresh = cv.threshold(dilation, 127, 255, 0)

    return thresh

# Get the intersection points when opposite sides is segmented into gridlines
def getIntersections(cornerPoints, segments=16):
    segments = 16
    n = segments
    c1, c2 = cornerPoints[0][0], cornerPoints[1][0]
    c3, c4 = cornerPoints[2][0], cornerPoints[3][0]
    intersections = []
    edgePoints = []
    for m in range(0, segments + 1):
        e1 = (m * c2 + n * c1) / (m + n)
        e2 = (m * c3 + n * c4) / (m + n)
        e3 = (m * c3 + n * c2) / (m + n)
        e4 = (m * c4 + n * c1) / (m + n)
        n = n - 1
        if m % 2 == 1:
            edgePoints.append([e1.astype(int), e2.astype(int)])
            edgePoints.append([e3.astype(int), e4.astype(int)])
            j = segments
            for i in range(0, segments + 1):
                i1 = (i * e2 + j * e1) / (i + j)
                if i % 2 == 1:
                    intersections.append(i1.astype(int))
                j = j - 1
    return intersections, edgePoints

# Finding contour with the maximum/minimum area above the threshold area
def getContour(contours, thresh=0, smallest=False):
    bigC = 0
    if smallest:
        temp = math.inf
    else:
        temp = 0
    index = 0
    for i in range(0, len(contours)):
        a = cv.contourArea(contours[i])
        if a > thresh:
            if (smallest and a < temp) or (not smallest and a > temp):
                bigC = contours[i]
                temp = a
                index = i
    return bigC, index

# Finding the center of the contour
def getCenter(contour):
    x, y, w, h = cv.boundingRect(contour)
    return [int(x + w / 2), int(y + h / 2)], x, y, w, h

# Mapping the point to the nearest intersection points (grid points)
def getNeighbour(point, intersections):
    temp = math.inf
    closestPoint = 0
    i = 0
    index = -1
    cX, cY = point[0], point[1]
    for points in intersections:
        pX, pY = points[0], points[1]
        dist = (cX - pX) ** 2 + (cY - pY) ** 2
        if temp > dist:
            closestPoint = [pX, pY]
            temp = dist
            index = i
        i = i + 1
    return closestPoint, index

# Approximate the contour into a quadrilateral
def getCorners(contour):
    epsilon = 0.1 * cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)
    return approx

# Returns the grid col and row index of the mapped point on the grid corresponding to the center of the contour in img
def getPosition(img, intersections):
    contours, hierarchy = cv.findContours(img, 1, 2)
    c = getContour(contours, 0, False)[0]
    # temp_img = np.zeros(np.shape(img))
    # rgb = temp_img.repeat(3).reshape(np.shape(img)[0], np.shape(img)[1], -1)
    # rgb = cv.drawContours(rgb, [c], -1, (0, 0, 255), 2)
    # showImage(rgb,1)
    c, x, y, w, h = getCenter(c)
    nP, index = getNeighbour(c, intersections)
    # col = 7 - math.floor(index / 8)
    # row = index % 8
    row = math.floor(index / 8)
    col = index % 8
    return (row, col), nP, c

# Function to find the stable frames in the video
def findStableFrames(video, refA, areaThreshold, stabilityFrame=50, UT=3000, LT=1000):
    movementFrames = [0]
    stableFrames = 0
    handing = False
    frameNo = 1
    for frame in video:
        thresh = getBlob(frame)
        contours, hierarchy = cv.findContours(thresh, 1, 2)
        c = getContour(contours, areaThreshold, True)[0]
        A = 0
        if type(c) != type(0):
            A = cv.contourArea(c)
        else:
            continue

        absDiff = abs(refA - A)
        if absDiff < LT and handing:
            stableFrames += 1
        elif absDiff > UT:
            handing = True
            stableFrames = 0
        else:
            stableFrames = 0

        if stableFrames == stabilityFrame:
            handing = False
            movementFrames.append(frameNo - int(stabilityFrame / 2))
            stableFrames = 0

        frameNo += 1

    return movementFrames

# Returns the final and orginal piece position as row and column index
def getPiecePos(img1, img2, intersections):
    # img1 = video[stableFrames[frameNo]]
    # img2 = video[stableFrames[frameNo + 1]]
    # m.showImage(img1)
    # m.showImage(img2)

    img1_blob = getBlob(img1)
    img2_blob = getBlob(img2)

    img12 = cv.subtract(img1_blob, img2_blob)
    img12_m = cv.medianBlur(img12, 15)
    # m.showImage(img12_m)
    # cv.imwrite("Results/img12.png",img12_m)
    img21 = cv.subtract(img2_blob, img1_blob)
    img21_m = cv.medianBlur(img21, 15)
    # cv.imwrite("Results/img21.png", img21_m)
    # m.showImage(img21_m)
    orgPos, nP1, orgC = getPosition(img12_m, intersections)
    finalPos, nP2, finalC = getPosition(img21_m, intersections)
    # m.showGraph(img1, intersections, edgePoints, c, nP)

    return orgPos, finalPos, orgC, finalC


def detectMovementAndUpdateBoard(img1, img2, intersections, chessboard):
    # print(orgPos)
    # print(finalPos)
    orgPos, finalPos, _, _ = getPiecePos(img1, img2, intersections)
    chessboard.movePiece(orgPos, finalPos)
    return chessboard.refresh()


def showImage(img, method=0):
    if method == 0:
        cv.imshow("frame", img)
        cv.waitKey(0)
    else:
        plt.imshow(img, cmap="gray")
        plt.show()


def showGraph(img, intersections, edgePoints, c, nP):
    temp_img = np.zeros(np.shape(img))
    rgb = temp_img.repeat(3).reshape(np.shape(img)[0], np.shape(img)[1], -1)
    for p in intersections:
        rgb = cv.circle(rgb, p, 10, (255, 0, 0), -1, cv.LINE_AA)
    for edge in edgePoints:
        rgb = cv.line(rgb, edge[0], edge[1], (0, 0, 255), 5, cv.LINE_AA)
    rgb = cv.circle(rgb, c, 5, (0, 255, 0), -1, cv.LINE_AA)
    rgb = cv.circle(rgb, nP, 5, (0, 0, 255), -1, cv.LINE_AA)
    size = np.shape(img)
    k = 0
    for p in intersections:
        row = math.floor(k / 8)
        col = k % 8
        rgb = cv.putText(rgb, "(" + str(row) + "," + str(col) + ")", p, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # rgb = cv.putText(rgb, str(k), p, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        k = k + 1
    showImage(cv.resize(rgb, (int(size[1] * 0.5), int(size[0] * 0.5))))
