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

def getMoments(img):
    mu = cv2.moments(img, False)
    x,y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
    return np.array([x,y])

def run(img):
    img_size = np.array([img.shape[1],img.shape[0]])
    print("Width: %d, Height: %d" % (img_size[0], img_size[1]))

    img_binalized = binalize(img)
    center = getMoments(img_binalized)

    error = center - img_size/2

    print("Position: [%d, %d]" % (center[0],center[1]))
    print("Error: [%d, %d]" % (error[0], error[1]))

    return error, center

if __name__ == '__main__':
    img = cv2.imread('./test/IMAGE_MOON3.JPG',1)
    error, center = run(img)

    cv2.circle(img, (center[0],center[1]), 4, 100, 2, 4)
    plt.imshow(img)
    plt.show()
