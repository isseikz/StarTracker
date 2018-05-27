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

    def updateData(self, x, xDot, xDt):
        self.x    = x
        self.xDot = xDot
        self.xDt  = xDt
        print(self.x)
        print(self.xDot)

    def getControlParam(self):
        pTerm = self.omega ** 2 * self.x
        dTerm = 2 * self.omega * self.zeta * self.xDot
        iTerm = self.kappa * self.xDt

        ctrlParam = -pTerm - dTerm - iTerm
        return ctrlParam


if __name__ == '__main__':
    model = cameraModel.CameraModel(cv2.imread('./test/IMAGE_MOON.JPG'))
    controller = PIDControl(0.8, 0.3, 0.2)

    error =[100,100] # huristic value
    pastError = [0,0]
    integralError = [0,0]
    while True:
        key = cv2.waitKey(100)&0xff
        if key == ord('s'):
            break

        error, center = binmom.run(model.currentImage)
        dError = np.array(error - pastError)
        integralError += error
        controller.updateData(error, dError, integralError)
        ctrl = controller.getControlParam()

        model.updateImage(*ctrl)
        model.showCurrentImage()
    else:
        model.showCurrentImage()
        cv2.waitKey(0)
