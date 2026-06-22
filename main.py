import numpy as np
from scipy.optimize import curve_fit, least_squares

from Electrode import WhiteNoise, Step
from HodgkinHuxley import HogdkinHuxley
from utils import sphereArea

def residuals(x, current, a, b, c):
    vPrime = test.runModel(x[0], current, a, b, c)[10, -1]
    print(vPrime)
    return (abs(-80) - abs(vPrime))
# They had two sorts of currents, 300 pA, 500 ms and -100 pA, 500 ms, Current from other paper 20 μA/cm2
#Toscana did 0.35 for steady state

#Optimize for steady state
test = HogdkinHuxley()
test.setValues()
current = WhiteNoise(0, 100)
# x0 = -5.614e+02
# bounds = [-3e-7 / sphereArea(5e-8), 3e-7 / sphereArea(5e-8)]
# result = least_squares(residuals, x0, bounds=bounds, args=[current, True, False, False])
# print(result)
#
# #Run steady state
I_hold = -5.614e+02
# z = test.runModel(I_hold, current, True, True, True)
# test.plotVoltageTimeSeries()
# test.plotAppliedCurrentTimeSeries()
# test.plotChannelTimeSeries()
# print("-------")
# print("m_CaT0 :" + str(z[0, -1]))
# print("m_CaH0 :" + str(z[1, -1]))
# print("m_KDR0 :" + str(z[2, -1]))
# print("m_KM0 :" + str(z[3, -1]))
# print("m_H0 :" + str(z[4, -1]))
# print("h_NaT0 :" + str(z[5, -1]))
# print("h_CaT0 :" + str(z[6, -1]))
# print("h_CaH0 :" + str(z[7, -1]))
# print("h_KDR0 :" + str(z[8, -1]))
# print("n_H0 :" + str(z[9, -1]))
# print("V0 :" + str(z[10, -1]))
# print("-------")
#Run step current
topCurrent = 3000
#3e-7 / sphereArea(5e-8)
current = Step(1500, 500, 0,topCurrent)
test.runModel(I_hold, current, True, True, True)
test.plotVoltageTimeSeries()
test.plotAppliedCurrentTimeSeries()
test.plotChannelTimeSeries()