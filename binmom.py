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
    mu = cv2.moments(img, False)
    x,y= int(mu["m10"]/mu["m00"]) ,int(mu["m01"]/mu["m00"])

    return np.array([x,y])

def run(img):
    img_size = np.array([img.shape[1],img.shape[0]])

    img_binalized = binalize(img)
    center = getCoG(img_binalized)
    error = center - img_size/2

    # print("Position: [%d, %d]" % (center[0],center[1]))
    # print("Error: [%d, %d]" % (error[0], error[1]))
    # print("Center: [%d, %d]" % (center[0], center[1]))

    cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)

    return error, center

if __name__ == '__main__':
    img = cv2.imread('./test/IMAGE_MOON.JPG',1)
    error, center = run(img)

    cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    plt.show()

    img = cv2.imread('./test/IMAGE_MOON2.JPG',1)
    error, center = run(img)

    cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    plt.show()

    img = cv2.imread('./test/IMAGE_MOON3.JPG',1)
    error, center = run(img)

    cv2.circle(img, (center[0],center[1]), int(img.shape[1] * 0.01), (0, 0, 255), -1)
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    plt.show()
