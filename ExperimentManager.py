import multiprocessing

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import least_squares
from scipy.signal import find_peaks

from Electrode import WhiteNoise, Chirp
from HodgkinHuxley import HogdkinHuxley
from ParallelFunctions import permute
from utils import sphereArea, residuals, printText


class ExperimentManager:
    def __init__(self, peakCurrent):
        self.experimentsRun = 0
        self.saveLocation = "./Out/"
        self.neuron = HogdkinHuxley()
        self.neuron.setValues_alt()
        # self.starting_I_hold =  -0.20956573344994844
        self.I_hold = -0.0047399334213286595
        # self.I_hold = -0.00020956573344785734
        self.peakCurrent = peakCurrent
    def run(self, experiment):
        # Optimize for steady state
        match experiment:
            case "Restart":
                self.neuron = HogdkinHuxley()
                self.neuron.setValues_alt()
                self.I_hold = self.starting_I_hold
            case "Optimize":
                print("Optimizing hold current and starting variables")
                x0 = 4
                current = WhiteNoise(0, 2000)
                result = least_squares(residuals, x0, args=[current, True, False, False, False, False, self.neuron], bounds=[-5,5], diff_step=0.1, xtol=1e-13) #You changed the scaling for g from 1000 to 1 and this shit has a tiny step size for some reason
                print("Hold current: " + str(result.x[0]))
                #Update initial gating variable
                self.I_hold = result.x[0]
                z = self.neuron.runModel(self.I_hold, current, True, False, False, True, False)
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
                # self.neuron.updateValues(z[0, -1], z[1, -1], z[2, -1], z[3, -1], z[4, -1], z[5, -1], z[6, -1], z[7, -1], z[8, -1], z[9, -1])
            case "Step":
                print("Running Step Experiment")
                # Run step current
                # current = WhiteNoise(0, 1000)
                # self.neuron.runModel(self.I_hold, current, True, False, False, True, True)
                current = WhiteNoise(0, 500)
                self.neuron.runModel(self.I_hold, current, True, False, True, True, False)
                # current = WhiteNoise(0, 500)
                # self.neuron.runModel(self.I_hold, current, True, False, True, True, True)
                current = WhiteNoise(self.peakCurrent, 500)
                self.neuron.runModel(self.I_hold, current, True, False, True, True, False)
                current = WhiteNoise(0, 500)
                self.neuron.runModel(self.I_hold, current, True, False, True, True, False)
                self.plotingSuite("Step Current " + str(self.peakCurrent * 100) + "pA for 500mS")
            case "Constant":
                print("Running Constant Current Experiment")
                # current = WhiteNoise(0, 3000)
                # self.neuron.runModel(self.I_hold, current, True, False, False, True, True)
                current = WhiteNoise(self.peakCurrent, 500)
                self.neuron.runModel(self.I_hold, current, True, True, True, True, True)
                self.plotingSuite("Constant Current " + str(self.peakCurrent * 100) + "pA")
                # self.neuron.plotChannelTimeSeriesVoltage()
            case "Chirp":
                # Run chirp current
                current = WhiteNoise(0, 1000)
                self.neuron.runModel(self.I_hold, current, True, False, False, True, True)
                current = Chirp(20 * 1000, self.peakCurrent)
                self.neuron.runModel(self.I_hold, current, True, False, True, True, True) #add step size 0.01
                self.plotingSuite("Chirp Current " + str(self.peakCurrent * 100) + "pA")
            case "PermutationTesting":
                #Create array of values to permute through. Starting with tau_m_CaT which has a default value of 2.
                permutationValues = self.generateValues(75)
                for permutationValue in permutationValues:
                    print(permutationValue)
                    self.neuron = HogdkinHuxley()
                    self.neuron.setValues_alt()
                    self.I_hold = 0
                    self.neuron.tau_m_KM = permutationValue

                    current = WhiteNoise(0, 500)
                    self.neuron.runModel(self.I_hold, current, True, False, False, True, False)
                    current = WhiteNoise(self.peakCurrent, 1000)
                    self.neuron.runModel(self.I_hold, current, True, False, True, True, False)

                    self.neuron.prepareToPlot()
                    self.neuron.plotVoltageTimeSeries(self.saveLocation, self.getPlotNumber(),True, True, "Varying tau_m_KM " + str(permutationValue))
                    # Plot spike timing
                    self.neuron.plotAdaptation(self.saveLocation, self.getPlotNumber(), "Varying tau_m_KM " + str(permutationValue))
                    self.experimentsRun += 1

            case "PermutationTesting2":
                # self.g_SK = 10  # * 1500# nS
                # self.k_SK = 0.8  # uM
                iterations = 100
                g_SK_Array = np.array(np.linspace(10 * 1e-6, 10 * 1e6, iterations))
                k_SK_Array = np.array(np.linspace(0.1 * 1e-6, 0.1 * 1e6, iterations))
                valueArray = np.zeros([iterations ** 2, 5])
                counter = 0
                for i, g_SK_value in enumerate(g_SK_Array):
                    for z, k_SK_value in enumerate(k_SK_Array):
                        counter +=1
                        valueArray[counter - 1] = [0, self.peakCurrent, counter, g_SK_value, k_SK_value]
                #valueArray = np.column_stack((np.full((len(g_SK_Array),1),self.starting_I_hold),np.full((len(g_SK_Array),1),self.peakCurrent), np.array(range(len(g_SK_Array))) + 1, g_SK_Array, k_SK_Array))
                pool_obj = multiprocessing.Pool()
                pool_obj.starmap(permute, valueArray)
                pool_obj.close()
                pool_obj.join()
            case "Debug":
                self.neuron.plotGatingPerVoltageTrace()
        self.experimentsRun += 1
    def plotingSuite(self, text):
        print("Ploting preparation")
        self.neuron.prepareToPlot()
        print("Printing title")
        printText(text, self.saveLocation, self.getPlotNumber())
        print("Printing voltage time series")
        self.neuron.plotVoltageTimeSeries(self.saveLocation, self.getPlotNumber())
        print("Printing applied current time series")
        self.neuron.plotAppliedCurrentTimeSeries(self.saveLocation, self.getPlotNumber())
        print("Printing gating variable time series")
        self.neuron.plotChannelTimeSeries(self.saveLocation, self.getPlotNumber())
        print("Printing channel current time series")
        self.neuron.plotChannelCurrentsTimeSeries(self.saveLocation, self.getPlotNumber())
        print("Printing calcium concentration time series")
        self.neuron.plotCalciumConcentration(self.saveLocation, self.getPlotNumber())
        print("Printing combined calcium current time series")
        self.neuron.plotCalciumCurrent(self.saveLocation, self.getPlotNumber())
        print("Adaptation")
        self.neuron.plotAdaptation(self.saveLocation, self.getPlotNumber())

    def getPlotNumber(self):
        return self.experimentsRun + 1

    def generateValues(self, mean, numberOfValues = 200):
        #Assume twenty plots and 20% on each side
        percentagePerSide = 0.90#0.2
        distanceFromMean = percentagePerSide * mean
        lowerBound = mean - distanceFromMean
        upperBound = mean + distanceFromMean
        return np.linspace(lowerBound, upperBound, numberOfValues)