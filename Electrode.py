import numpy as np
from scipy.signal import chirp
#This class serves to return the voltage at any time point
class Electrode:
    #Initialize the class, takes two arguments 1. The value of the current, 2. The length of the run
    def __init__(self, current, length):
        self.current = current
        self.length = length
    #Returns the length of the run
    def getLength(self):
        return self.length
    #Gets the current for multiple time points
    def getMultipleCurrents(self, t_eval):
        t = np.array([])
        for time in t_eval:
            t = np.append(t, self.getCurrent(time))
        return t
    #Returns the current for one time point
    def getCurrent(self, t):
        raise NotImplementedError("Must be implemented in subclass")
#Constant steady current
class Steady(Electrode):
    #Returns the current for one time point
    def getCurrent(self, t):
        return self.current
#An oscilating sine wave from 0-15Hz. Accepts two arguments: 1. Length of the run, 2. The max amplitude of the current
class Chirp(Electrode):
    def __init__(self, length, top):
        self.length = length
        self.top = top
        self.scalingFactor = 1000
        super().__init__(None, length)
    #Calculate and returns the current for one timepoint
    def getCurrent(self, t):
        return abs(chirp(t, 0, self.length,15/(self.scalingFactor * 2), method='linear', phi=90)) * self.top
