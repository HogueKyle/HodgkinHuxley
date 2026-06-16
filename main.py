from Electrode import WhiteNoise
from HodgkinHuxley import HogdkinHuxley

test = HogdkinHuxley()
test.setValues()
current = WhiteNoise(10, 100)
test.runModel(current)
test.plotVoltageTimeSeries()