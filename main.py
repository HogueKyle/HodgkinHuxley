from Electrode import WhiteNoise
from VoltageClamp import VoltageClamp

test = VoltageClamp()
test.setValues()
current = WhiteNoise(10, 1000)
test.runModel(current)