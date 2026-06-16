import numpy as np

class WhiteNoise:
    def __init__(self, current, length):
        self.current = current
        self.length = length
    def getCurrent(self, t):
        return self.current
    def getMultipleCurrents(self, t_eval):
        t = np.array([])
        for time in t_eval:
            np.append(t, self.getCurrent(time))
        return t
    def getLength(self):
        return self.length