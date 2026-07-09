import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import least_squares

from Electrode import WhiteNoise, Chirp
from HodgkinHuxley import HogdkinHuxley
from utils import sphereArea, residuals


class ExperimentManager:
    def __init__(self):
        self.experimentsRun = 0
        self.saveLocation = "./Plots/"
        self.neuron = HogdkinHuxley()
        self.neuron.setValues_alt()
        self.starting_I_hold =  -0.20956573344994844
        self.I_hold = self.starting_I_hold
        # self.I_hold = -0.00020956573344785734
    def run(self, experiment):
        # Optimize for steady state
        match experiment:
            case "Restart":
                self.neuron = HogdkinHuxley()
                self.neuron.setValues_alt()
                self.I_hold = self.starting_I_hold
            case "Optimize":
                print("Optimizing hold current and starting variables")
                x0 = -5
                current = WhiteNoise(0, 1000)
                result = least_squares(residuals, x0, args=[current, True, False, False, False, self.neuron], bounds=[-5,5], diff_step=0.1, xtol=1e-13) #You changed the scaling for g from 1000 to 1 and this shit has a tiny step size for some reason
                print("Hold current: " + str(result.x[0]))
                #Update initial gating variable
                self.I_hold = result.x[0]
                z = self.neuron.runModel(self.I_hold, current, True, False, False, False)
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
                self.neuron.updateValues(z[0, -1], z[1, -1], z[2, -1], z[3, -1], z[4, -1], z[5, -1], z[6, -1], z[7, -1], z[8, -1], z[9, -1])
            case "Step":
                print("Running Step Experiment")
                # Run step current
                topCurrent = 2
                current = WhiteNoise(0, 1000)
                self.neuron.runModel(self.I_hold, current, True, False, True, True)
                current = WhiteNoise(0, 500)
                self.neuron.runModel(self.I_hold, current, True, True, True, True)
                current = WhiteNoise(topCurrent, 500)
                self.neuron.runModel(self.I_hold, current, True, True, True, True)
                current = WhiteNoise(0, 500)
                self.neuron.runModel(self.I_hold, current, True, True, True, True)
                self.plotingSuite("Step Current 200pA for 500mS")
            case "Constant":
                print("Running Constant Current Experiment")
                #current = WhiteNoise(0, 1000)
                #self.neuron.runModel(self.I_hold, current, True, False, True, False)
                # topCurrent =  1.5e-7 / sphereArea(0.0028)
                # topCurrent =  3e-7 / sphereArea(0.0025)
                topCurrent = 2 #2 and 3
                current = WhiteNoise(0, 1000)
                self.neuron.runModel(self.I_hold, current, True, False, True, True)
                current = WhiteNoise(topCurrent, 500)
                self.neuron.runModel(self.I_hold, current, True, True, True, True)
                self.plotingSuite("Constant Current 200pA")
            case "Chirp":
                # Run chirp current
                topCurrent = 2
                current = WhiteNoise(0, 1000)
                self.neuron.runModel(self.I_hold, current, True, False, True, True)
                current = Chirp(20 * 1000, topCurrent)
                self.neuron.runModel(self.I_hold, current, True, True, True, True) #add step size 0.01
                self.plotingSuite("Chirp Current 200pA")
            case "PermutationTesting":
                #Create array of values to permute through. Starting with tau_m_CaT which has a default value of 2.
                topCurrent = 1
                permutationValues = self.generateValues(75)
                for permutationValue in permutationValues:
                    print(permutationValue)
                    self.neuron = HogdkinHuxley()
                    self.neuron.setValues_alt()
                    self.I_hold = self.starting_I_hold
                    self.neuron.tau_m_KM = permutationValue #Needs to be changed back
                    #Get rid of transient
                    current = WhiteNoise(0, 1000)
                    self.neuron.runModel(self.I_hold, current, True, False, True, False)
                    #Run model
                    current = WhiteNoise(topCurrent, 500*10)
                    self.neuron.runModel(self.I_hold, current, True, True, True, False)
                    self.neuron.prepareToPlot()
                    self.neuron.plotVoltageTimeSeries(self.saveLocation, self.getPlotNumber(),False, True, "Varying kn_H " + str(permutationValue))
                #plt.savefig(self.saveLocation + str(self.getPlotNumber()) + ".Channel Current Timeseries" + str(self.getPlotNumber()) + ".png")
                #plt.show()
        self.experimentsRun += 1
    def plotingSuite(self, text):
        print("Ploting preparation")
        self.neuron.prepareToPlot()
        print("Printing title")
        self.printText(text, self.saveLocation, self.getPlotNumber())
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

    def printText(self, text, saveLocation, saveNumber):
        plt.text(0.5,0.5, text, fontsize=20, horizontalalignment="center", verticalalignment="center", fontstretch="ultra-expanded")
        plt.axis('off')
        plt.savefig(saveLocation + str(saveNumber) + ".Experiment Title" + ".png")
        plt.show()

    def getPlotNumber(self):
        return self.experimentsRun + 1

    def generateValues(self, mean):
        #Assume twenty plots and 20% on each side
        numberOfValues = 40
        percentagePerSide = 0.70#0.2
        distanceFromMean = percentagePerSide * mean
        lowerBound = mean - distanceFromMean
        upperBound = mean + distanceFromMean
        return np.linspace(lowerBound, upperBound, numberOfValues)