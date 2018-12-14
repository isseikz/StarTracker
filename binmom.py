#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import math
from matplotlib import pyplot as plt

def binalize(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = 60
    max_pixel = 255
    ret, img_binalized = cv2.threshold(img_gray,
                                 thresh,
                                 max_pixel,
                                 cv2.THRESH_BINARY)
    return img_binalized

def getCoG(img):
    img_size = np.array([img.shape[1],img.shape[0]])
    mu = cv2.moments(img, False)
    if mu["m00"] < 1.0e-2:
        # cv2.imshow("image",img)
        x = int(img_size[0]/2)
        y = int(img_size[1]/2)
    else:
        x,y= int(mu["m10"]/mu["m00"]) ,int(mu["m01"]/mu["m00"])

        pass

    return np.array([x,y])

def run(img):
    img_size = np.array([img.shape[1],img.shape[0]])

    img_binalized = binalize(img)
    center = getCoG(img_binalized)
    error = center - img_size/2

    print("Position: [%d, %d]" % (center[0],center[1]))
    print("Error: [%d, %d]" % (error[0], error[1]))
    print("Center: [%d, %d]" % (center[0], center[1]))

    cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)

    return error, center

def runMovingObject(img, pastImg):
    img_size = np.array([img.shape[1],img.shape[0]])

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    pastGray = cv2.cvtColor(pastImg, cv2.COLOR_RGB2GRAY)

    # cv2.accumulateWeighted(gray, pastGray, 0.5)
    delta = cv2.absdiff(gray, pastGray)

    ret, img_binalized = cv2.threshold(delta, 100, 255, cv2.THRESH_BINARY)
    center = getCoG(img_binalized)
    error = center - img_size/2

    print("Position: [%d, %d]" % (center[0],center[1]))
    print("Error: [%d, %d]" % (error[0], error[1]))
    print("Center: [%d, %d]" % (center[0], center[1]))

    cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)

    return error, center

def runPink(img):
    img_size = np.array([img.shape[1],img.shape[0]])

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv
    lowerPink = np.array([150, 150, 20])
    upperPink = np.array([170, 255, 255])
    imgMask = cv2.inRange(imgHSV, lowerPink, upperPink)
    imgMasked =  cv2.bitwise_and(img, img, mask=imgMask)
    # plt.figure()
    # plt.imshow(cv2.cvtColor(imgMasked, cv2.COLOR_RGB2BGR))
    # plt.show()

    img_gray = cv2.cvtColor(imgMasked, cv2.COLOR_RGB2GRAY)
    ret, img_binalized = cv2.threshold(img_gray, 60, 255, cv2.THRESH_BINARY)
    # plt.figure()
    # plt.imshow(cv2.cvtColor(img_binalized, cv2.COLOR_RGB2BGR))
    # plt.show()
    center = getCoG(img_binalized)
    error = center - img_size/2

    print("Position: [%d, %d]" % (center[0],center[1]))
    print("Error: [%d, %d]" % (error[0], error[1]))
    print("Center: [%d, %d]" % (center[0], center[1]))

    cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)

    return error, center

if __name__ == '__main__':
    img = cv2.imread('./20180707test/out599.jpg',1)
    error, center = runPink(img)

    cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    plt.show()

    # img = cv2.imread('./test/IMAGE_MOON.JPG',1)
    # error, center = run(img)
    #
    # cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)
    # plt.figure()
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    # plt.show()
    #
    # img = cv2.imread('./test/IMAGE_MOON2.JPG',1)
    # error, center = run(img)
    #
    # cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)
    # plt.figure()
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    # plt.show()
    #
    # img = cv2.imread('./test/IMAGE_MOON3.JPG',1)
    # error, center = run(img)
    #
    # cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)
    # plt.figure()
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    # plt.show()
