import numpy as np
import cv2
import math
from matplotlib import pyplot as plt

import binmom

class CameraModel(object):
    """docstring for CameraModel."""
    def __init__(self, ii):
        super(CameraModel, self).__init__()
        self.initialImage   = ii
        self.currentImage   = ii
        self.planetVelocity = [10,-2] # [pixel/step]
        # self.planetVelocity = [0,0] # [pixel/step]
        self.imageSize      = tuple(np.array([self.initialImage.shape[1], self.initialImage.shape[0]]))
        self.position       = [0,0]
        self.gearRate       = 1.5

    def updateImage(self, posdX, posdY):
        print([posdX,posdY])
        self.position[0] += posdX * self.gearRate + self.planetVelocity[0]
        self.position[1] += posdY * self.gearRate + self.planetVelocity[1]
        rad = 0
        matrix = [
        [np.cos(rad), -np.sin(rad), self.position[0]],
        [np.sin(rad), np.cos(rad),  self.position[1]]
        ]
        affineMatrix = np.float32(matrix)
        self.currentImage = cv2.warpAffine(self.initialImage, affineMatrix, self.imageSize,flags=cv2.INTER_NEAREST)

    def showCurrentImage(self):
        cv2.namedWindow('Current Image', cv2.WINDOW_NORMAL)

        outputImage = self.currentImage.copy() #OpenCV は別の変数に代入しても，元の変数を改変するため，.copy()関数でクローンを作成する
        cv2.line(outputImage, (self.imageSize[0]//2,self.imageSize[1]//2-20), (self.imageSize[0]//2,self.imageSize[1]//2+20), (200, 200, 200),thickness=3, lineType=cv2.LINE_AA)
        cv2.line(outputImage, (self.imageSize[0]//2-20,self.imageSize[1]//2), (self.imageSize[0]//2+20,self.imageSize[1]//2), (200, 200, 200),thickness=3,lineType=cv2.LINE_AA)
        cv2.putText(outputImage, 'X POSITION: ' + str(self.position[0]), (40, 70), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(outputImage, 'Y POSITION: ' + str(self.position[1]), (40, 120), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(outputImage, 'STOP: \'s\'', (40, 170), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(outputImage, 'CONTROL: \'jil,\'', (40, 220), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.imshow('Current Image',outputImage)


if __name__ == '__main__':
    threshold = 0
    model = CameraModel(cv2.imread('./test/IMAGE_MOON.JPG'))

    c = 'o'
    ctrl = [0,0]
    while True:
        key = cv2.waitKey(100)&0xff
        if key == ord('s'):
            break
        elif key == ord('l'):
            ctrl[0] += 10
        elif key == ord('j'):
            ctrl[0] += -10
        elif key == ord('i'):
            ctrl[1] += 10
        elif key == ord(','):
            ctrl[1] += -10
        else:
            ctrl = [0,0]

        error, center = binmom.run(model.currentImage)
        ctrl = -1.2 * error

        model.updateImage(*ctrl)
        model.showCurrentImage()
