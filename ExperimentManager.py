from scipy.optimize import least_squares

from Electrode import WhiteNoise, Step, Chirp
from HodgkinHuxley import HogdkinHuxley
from utils import sphereArea, residuals


class ExperimentManager:
    def __init__(self):
        self.test = HogdkinHuxley()
        self.test.setValues_alt()
        self.I_hold = -0.20956368313672644
    def run(self, experiment):
        # Optimize for steady state
        match experiment:
            case "Optimize":
                print("Optimizing hold current and starting variables")
                x0 = -5
                current = WhiteNoise(0, 1000)
                result = least_squares(residuals, x0, args=[current, True, False, False, False, self.test], bounds=[-5,5], diff_step=0.1, xtol=1e-13) #You changed the scaling for g from 1000 to 1 and this shit has a tiny step size for some reason
                print("Hold current: " + str(result.x[0]))
                #Update initial gating variable
                self.I_hold = result.x[0]
                z = self.test.runModel(self.I_hold, current, True, False, False, False)
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
                self.test.updateValues(z[0, -1], z[1, -1], z[2, -1], z[3, -1], z[4, -1], z[5, -1], z[6, -1], z[7, -1], z[8, -1], z[9, -1])
            case "Step":
                print("Running Step Experiment")
                # Run step current
                topCurrent = 3000
                # 3e-7 / sphereArea(5e-8)
                current = WhiteNoise(0, 500)
                self.test.runModel(self.I_hold, current, True, True, True, True)
                current = WhiteNoise(topCurrent, 500)
                self.test.runModel(self.I_hold, current, True, True, True, True)
                current = WhiteNoise(0, 500)
                self.test.runModel(self.I_hold, current, True, True, True, True)
                self.test.plotVoltageTimeSeries()
                self.test.plotAppliedCurrentTimeSeries()
                self.test.plotChannelTimeSeries()
            case "Constant":
                print("Running Constant Current Experiment")
                current = WhiteNoise(0, 1000)
                self.test.runModel(self.I_hold, current, True, False, True, False)
                #topCurrent = 1.5e-7 / sphereArea(0.0028)
                topCurrent = 50
                current = WhiteNoise(topCurrent, 500)
                self.test.runModel(self.I_hold, current, True, True, True, True)
                self.test.plotVoltageTimeSeries()
                self.test.plotAppliedCurrentTimeSeries()
                self.test.plotChannelTimeSeries()
                self.test.plotChannelCurrentsTimeSeries()
            case "Chirp":
                # Run chirp current
                topCurrent = 1.5e-7 / sphereArea(0.0028)
                current = Chirp(30 * 1000, 0, 15, 0, topCurrent)
                self.test.runModel(self.I_hold, current, True, True, True, True)
                self.test.plotVoltageTimeSeries()
                self.test.plotAppliedCurrentTimeSeries()
                self.test.plotChannelTimeSeries()