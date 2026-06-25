from scipy.optimize import least_squares

from Electrode import WhiteNoise, Step, Chirp
from HodgkinHuxley import HogdkinHuxley
from utils import sphereArea, residuals


class ExperimentManager:
    def __init__(self, type):
        self.type = type
    def run(self):
        # Optimize for steady state
        test = HogdkinHuxley()
        test.setValues()
        current = WhiteNoise(0, 1000)
        I_hold = -2.306727847622885e-06
        #test.runModel(I_hold, current, True, False, True)
        match self.type:
            case "Optimize":
                x0 = -2.306727847622885e-06
                bounds = [-3e-7 / sphereArea(5e-8), 3e-7 / sphereArea(5e-8)]
                result = least_squares(residuals, x0, bounds=bounds, args=[current, True, False, False, test])
                print("Hold current: " + str(result.x[0]))
                print(str(result))
                I_hold = result.x[0]
                z = test.runModel(I_hold, current, True, True, False)
                test.plotVoltageTimeSeries()
                test.plotAppliedCurrentTimeSeries()
                test.plotChannelTimeSeries()
                print("-------")
                print("m_CaT0 :" + str(z[0, -1]))
                print("m_CaH0 :" + str(z[1, -1]))
                print("m_KDR0 :" + str(z[2, -1]))
                print("m_KM0 :" + str(z[3, -1]))
                print("m_H0 :" + str(z[4, -1]))
                print("h_NaT0 :" + str(z[5, -1]))
                print("h_CaT0 :" + str(z[6, -1]))
                print("h_CaH0 :" + str(z[7, -1]))
                print("h_KDR0 :" + str(z[8, -1]))
                print("n_H0 :" + str(z[9, -1]))
                print("V0 :" + str(z[10, -1]))
                print("-------")
            case "Step":
                print("Running Step Experiment")
                # Run step current
                topCurrent = 3000
                # 3e-7 / sphereArea(5e-8)
                current = WhiteNoise(0, 500)
                test.runModel(I_hold, current, True, True, True)
                current = WhiteNoise(topCurrent, 500)
                test.runModel(I_hold, current, True, True, True)
                current = WhiteNoise(0, 500)
                test.runModel(I_hold, current, True, True, True)
                test.plotVoltageTimeSeries()
                test.plotAppliedCurrentTimeSeries()
                test.plotChannelTimeSeries()
            case "Constant":
                test.runModel(I_hold, current, True, False, True)
                print("Running Constant Current Experiment")
                # Run step current
                #topCurrent = 0.1
                topCurrent = 1.5e-7 / sphereArea(0.0028)
                # topCurrent = 1
                current = WhiteNoise(topCurrent, 500)
                test.runModel(I_hold, current, True, True, True)
                test.plotVoltageTimeSeries()
                test.plotAppliedCurrentTimeSeries()
                test.plotChannelTimeSeries()
            case "Chirp":
                # Run chirp current
                topCurrent = 3000
                # 3e-7 / sphereArea(5e-8)
                current = Chirp(30 * 1000, 0, 15, 0, topCurrent)
                test.runModel(I_hold, current, True, True, True)
                test.plotVoltageTimeSeries()
                test.plotAppliedCurrentTimeSeries()
                test.plotChannelTimeSeries()

    # def residuals(x, current, a, b, c):
    #     vPrime = test.runModel(x[0], current, a, b, c)[10, -1]
    #     print(vPrime)
    #     return (abs(-80) - abs(vPrime))