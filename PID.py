#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

import cameraModel
import binmom

class PIDControl(object):
    """docstring for PDControl."""
    def __init__(self, omega, zeta, kappa):
        super(PIDControl, self).__init__()
        self.xDot     = np.array([0,0])
        self.x        = np.array([0,0])
        self.xDt      = np.array([0,0])
        self.omega    = omega
        self.zeta     = zeta
        self.kappa    = kappa

    def updateData(self, x):
        self.xDot = x - self.x
        self.xDt  = x + self.xDt
        self.x    = x

    def getControlParam(self):
        pTerm = self.omega ** 2 * self.x
        dTerm = 2 * self.omega * self.zeta * self.xDot
        iTerm = self.kappa * self.xDt

        ctrlParam = -pTerm - dTerm - iTerm
        return ctrlParam


if __name__ == '__main__':
    model = cameraModel.CameraModel(cv2.imread('./test/IMAGE_MOON.JPG'))
    controller = PIDControl(0.5, 0.3, 0.3)

    error =[100,100] # huristic value
    error2 = 0
    pastError = [0,0]
    integralError = [0,0]
    while np.linalg.norm(error) > 1.0e-3:
        key = cv2.waitKey(100)&0xff
        if key == ord('s'):
            break

        error, center = binmom.run(model.currentImage)
        controller.updateData(error)
        ctrl = controller.getControlParam()

        error2 += np.linalg.norm(error)
        model.updateImage(*ctrl)
        model.showCurrentImage(error2)

    cv2.waitKey(0)
