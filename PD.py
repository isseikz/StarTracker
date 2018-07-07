#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

import cameraModel
import binmom

class PDControl(object):
    """docstring for PDControl."""
    def __init__(self, omega, zeta):
        super(PDControl, self).__init__()
        self.xDot     = np.array([0,0])
        self.x        = np.array([0,0])
        self.omega    = omega
        self.zeta     = zeta

    def updateData(self, x):
        self.xDot = x - self.x
        self.x    = x

    def getControlParam(self):
        pTerm = self.omega ** 2 * self.x
        dTerm = 2 * self.omega * self.zeta * self.xDot

        ctrlParam = -pTerm - dTerm
        return ctrlParam


if __name__ == '__main__':
    model = cameraModel.CameraModel(cv2.imread('./test/IMAGE_MOON.JPG'))
    controller = PDControl(0.5, 0.3)

    error2 = 0
    error =[100,100] # huristic value
    while np.linalg.norm(error) > 1.0e-3:
        key = cv2.waitKey(100)&0xff
        if key == ord('s'):
            break

        error, center = binmom.run(model.currentImage)
        controller.updateData(error)
        ctrl = controller.getControlParam()

        model.updateImage(*ctrl)

        error2 += np.linalg.norm(error)
        model.showCurrentImage(error2)
