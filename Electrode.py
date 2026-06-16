import numpy as np

class WhiteNoise:
    def __init__(self, current, length):
        self.current = current
        self.length = length
    def getCurrent(self, t):
        return self.current
    def getLength(self):
        return self.length