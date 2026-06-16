from Electrode import WhiteNoise, Step
from HodgkinHuxley import HogdkinHuxley

test = HogdkinHuxley()
test.setValues()
current = WhiteNoise(10, 100)
test.runModel(current)
test.plotVoltageTimeSeries()
test.plotAppliedCurrentTimeSeries()
current = Step(1000, 50, 10, 100)
test.runModel(current)
test.plotVoltageTimeSeries()
test.plotAppliedCurrentTimeSeries()