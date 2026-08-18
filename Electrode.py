import numpy as np
from scipy.signal import chirp


class Electrode:
    def __init__(self, current, length):
        self.current = current
        self.length = length
    def getLength(self):
        return self.length
    def getMultipleCurrents(self, t_eval):
        t = np.array([])
        for time in t_eval:
            t = np.append(t, self.getCurrent(time))
        return t
    def getCurrent(self, t):
        raise NotImplementedError("Must be implemented in subclass")
class Steady(Electrode):
    def getCurrent(self, t):
        return self.current
class Step(Electrode):
    def __init__(self, length, stepTime, bottom, top):
        self.length = length
        self.stepTime = stepTime
        self.bottom = bottom
        self.top = top
        super().__init__(None, length)
    def getCurrent(self, t):
        position = "bottom"
        leftBorder = 0
        rightBorder = self.stepTime
        while self.stepTime <= self.length:
            if (t >= leftBorder and t < rightBorder):
                if position == "bottom":
                    return self.bottom
                else:
                    return self.top
            else:
                leftBorder = rightBorder
                rightBorder = rightBorder + self.stepTime
                if position == "bottom":
                    position = "top"
                else:
                    position = "bottom"
class Chirp(Electrode):
    def __init__(self, length, top):
        self.length = length
        self.top = top
        self.scalingFactor = 1000
        super().__init__(None, length)
    def getCurrent(self, t):
        return abs(chirp(t, 0, self.length,15/(self.scalingFactor * 2), method='linear', phi=90)) * self.top
