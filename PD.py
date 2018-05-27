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

    def updateData(self, x, xDot):
        self.x    = x
        self.xDot = xDot
        print(self.x)
        print(self.xDot)

    def getControlParam(self):
        pTerm = self.omega ** 2 * self.x
        dTerm = 2 * self.omega * self.zeta * self.xDot

        ctrlParam = -pTerm - dTerm
        return ctrlParam


if __name__ == '__main__':
    model = cameraModel.CameraModel(cv2.imread('./test/IMAGE_MOON.JPG'))
    controller = PDControl(0.8, 0.3)

    error =[100,100] # huristic value
    pastError = [0,0]
    while True:
        key = cv2.waitKey(100)&0xff
        if key == ord('s'):
            break

        error, center = binmom.run(model.currentImage)
        dError = np.array(error - pastError)
        controller.updateData(error, dError)
        ctrl = controller.getControlParam()

        model.updateImage(*ctrl)
        model.showCurrentImage()
    else:
        model.showCurrentImage()
        cv2.waitKey(0)
