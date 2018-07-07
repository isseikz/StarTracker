#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

class gainCTRL():
    """Optimal control law updating the control gains from the residual of the planet position after step."""
    def __init__(self):
        """Set the initial control gains"""
        self.matGain=np.matrix([
        [1.0, 0.0],
        [0.0, 1.0]
        ])
        self.controlSteps = np.matrix([0.0,0.0]).T

    def updateGain(self, steps, errors):
        """Update the control gains. It returns the updated gains"""
        if np.linalg.norm(steps) > 1.0e-3:
            dA = np.matrix([
            [steps[0,0]*errors[0,0],steps[1,0]*errors[0,0]],
            [steps[0,0]*errors[1,0],steps[1,0]*errors[1,0]]
            ])/(steps[0,0]**2 + steps[1,0]**2)
        else:
            dA = np.zeros([2,2])

        # print(self.matGain)
        self.matGain = np.linalg.inv(self.matGain) + dA
        return self.matGain

    def calcSteps(self, errors):
        """Calculate the motor steps from the position errors of the planet. Return the control steps[steps]"""
        self.controlSteps = self.matGain * errors
        return self.controlSteps

    def gain(self):
        """Return current control gains"""
        return self.matGain

if __name__ == '__main__':
    """Check the convergence and gain optimizing assuming the target is stationally."""
    g = gainCTRL()
    errors = np.matrix([100,50]).T
    step2dist = np.matrix([
    [1.5,0],
    [0,1.5]
    ])

    while np.linalg.norm(errors) > 1.0e-3:
        steps  = g.calcSteps(errors)
        errors = errors - step2dist * steps

        g.updateGain(steps,errors)
        print("step: %d,%d error: %d,%d" % (steps[0,0],steps[1,0],errors[0,0],errors[1,0]))

    print(g.gain())
