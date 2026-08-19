import multiprocessing
import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import least_squares
from Electrode import Steady, Chirp
from HodgkinHuxley import HogdkinHuxley
from ParallelFunctions import permute
from utils import residuals, printText


class ExperimentManager:
    #Initialize class
    def __init__(self, peakCurrent, modelType, saveLocation = "./Out/"):
        self.experimentsRun = 0
        self.modelType = modelType
        self.saveLocation = saveLocation
        self.I_hold = 0
        self.starting_I_hold = self.I_hold
        self.peakCurrent = peakCurrent
        #Create model according to set type
        self.neuron = HogdkinHuxley()
        self.neuron.setValues_alt(self.modelType)
        #Make output folder if necessary
        if not os.path.exists(self.saveLocation):
            os.makedirs(self.saveLocation)
        #Determine what channels to use according to model type
        self.useSK = True
        self.useH = True
        match self.modelType:
            case "Nowacki":
                self.useSK = False
                self.useH = False
            case "Saghafi":
                self.useSK = False
                self.useH = True
            case "Saghafi_DE":
                self.useSK = False
                self.useH = True
            case "Calcium":
                self.useSK = True
                self.useH = True
            case "Saghafi_M":
                self.useSK = False
                self.useH = True
    def run(self, experiment):
        ##Run the correct experiment
        match experiment:
            #Replace the current HH model with a fresh version
            case "Restart":
                self.neuron = HogdkinHuxley()
                self.neuron.setValues_alt(self.modelType)
                self.I_hold = self.starting_I_hold
            #Optimize the model for a specific hold voltage. Model will print gating variables resulting in desired hold, as well as update starting values so subsequent experiments will start from this state.
            case "Optimize":
                print("Optimizing hold current and starting variables")
                x0 = 4
                current = Steady(0, 2000)
                result = least_squares(residuals, x0, args=[current, True, self.useSK, self.useH, False, False, False, self.neuron], bounds=[-5,5], diff_step=0.1, xtol=1e-13)
                print("Hold current: " + str(result.x[0]))
                #Update initial gating variable
                self.I_hold = result.x[0]
                z = self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH,False, True, False)
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
            #Run a 500ms step current experiment (500ms no current, 500ms current of amplitude set in main, 500ms no current)
            case "Step":
                print("Running Step Experiment")
                # Run to steady state
                # current = Steady(0, 30000)
                # self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH, False, True, False)
                # Run no current
                current = Steady(0, 500)
                self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH, True, True, False)
                #Run specified current (up stroke of step)
                current = Steady(self.peakCurrent, 500)
                self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH, True, True, False)
                #Run no current
                current = Steady(0, 500)
                self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH, True, True, False)
                #Plot results
                self.plotingSuite("Step Current " + str(self.peakCurrent * 100) + "pA for 500mS")
            #Inject a constant current into the neuron for 5 seconds.
            case "Constant":
                print("Running Constant Current Experiment")
                # Run to steady state
                current = Steady(0, 30000)
                self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH, False, True, False)
                #Inject constant current
                current = Steady(0, 5000)
                self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH, True, True, False)
                #Plot results
                self.plotingSuite("Constant Current " + str(self.peakCurrent * 100) + "pA")
            # Inject a chirp current 0-15Hz in 20 seconds
            case "Chirp":
                # Run to steady state
                current = Steady(0, 30000)
                self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH, False, True, False)
                #Inject chirp current
                current = Chirp(20 * 1000, self.peakCurrent)
                self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH, True, True, False)
                #Plot results
                self.plotingSuite("Chirp Current " + str(self.peakCurrent * 100) + "pA")
            #Generate a voltage and adaptation plot for an array of values for one parameter. Currently set for tau_m_KM, can be modified to any other parameter.
            case "PermutationTesting":
                #Generate a distrubution of values to permute over for a parameter
                permutationValues = self.generateValues(75)
                #Generate plots for each value in the array
                for permutationValue in permutationValues:
                    print(permutationValue)
                    self.neuron = HogdkinHuxley()
                    self.neuron.setValues_alt(self.modelType)
                    self.neuron.tau_m_KM = permutationValue
                    # Run to steady state
                    current = Steady(0, 30000)
                    self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH, False, True, False)
                    # Inject constant current
                    current = Steady(0, 5000)
                    self.neuron.runModel(self.I_hold, current, True, self.useSK, self.useH, True, True, False)
                    #Plot results
                    self.neuron.prepareToPlot()
                    self.neuron.plotVoltageTimeSeries(self.saveLocation, self.getPlotNumber(),False, True, "Varying tau_m_KM ",  str(permutationValue))
                    self.neuron.plotAdaption(self.saveLocation, self.getPlotNumber(), "Varying tau_m_KM ", str(permutationValue))
                    self.experimentsRun += 1
                plt.legend(loc="upper right")
                plt.show()
            #Create multiple plots for two parameters searching across two arrays
            case "PermutationTesting2":
                #Number of values to try for EACH parameter
                iterations = 22
                #Create array of values to search across
                g_SK_Array = np.array(np.linspace(0, 10000, iterations))
                k_SK_Array = np.array(np.linspace(0, 10000, iterations))
                valueArray = np.zeros([iterations ** 2, 5])
                #Pass model type
                modelType = 0
                match self.modelType:
                    case "Nowacki":
                        modelType = 0
                    case "Saghafi":
                        modelType = 1
                    case "Saghafi_DE":
                        modelType = 2
                    case "Calcium":
                        modelType = 3
                    case "Saghafi_M":
                        modelType = 4
                #Search using 'permute' in ParallelFunctions.py
                counter = 0
                for i, g_SK_value in enumerate(g_SK_Array):
                    for z, k_SK_value in enumerate(k_SK_Array):
                        counter +=1
                        valueArray[counter - 1] = [self.starting_I_hold, self.peakCurrent, counter, g_SK_value, k_SK_value, modelType]
                pool_obj = multiprocessing.Pool()
                pool_obj.starmap(permute, valueArray)
                pool_obj.close()
                pool_obj.join()
        self.experimentsRun += 1
    #Print plots for each experiment
    def plotingSuite(self, text):
        # print("Ploting preparation")
        self.neuron.prepareToPlot()
        # print("Printing title")
        printText(text, self.saveLocation, self.getPlotNumber())
        # print("Printing voltage time series")
        self.neuron.plotVoltageTimeSeries(self.saveLocation, self.getPlotNumber())
        # print("Printing applied current time series")
        self.neuron.plotAppliedCurrentTimeSeries(self.saveLocation, self.getPlotNumber())
        # print("Printing gating variable time series")
        self.neuron.plotChannelTimeSeries(self.saveLocation, self.getPlotNumber())
        # print("Printing channel current time series")
        self.neuron.plotChannelCurrentsTimeSeries(self.saveLocation, self.getPlotNumber())
        # print("Printing spike frequency adaptation plot")
        self.neuron.plotAdaption(self.saveLocation, self.getPlotNumber())
        if self.modelType == "Calcium":
            # print("Printing calcium concentration time series")
            self.neuron.plotCalciumConcentration(self.saveLocation, self.getPlotNumber())
            # print("Printing combined calcium current time series")
            self.neuron.plotCalciumCurrent(self.saveLocation, self.getPlotNumber())
    #Increment and return the current plot number for saving
    def getPlotNumber(self):
        return self.experimentsRun + 1
    #Generate an array of values centered around a value. Takes 0.3 of the value and uses that to create the upper and lower bound of the distribution.
    def generateValues(self, mean, numberOfValues = 10, percentagePerSide = 0.30):
        distanceFromMean = percentagePerSide * mean
        lowerBound = mean - distanceFromMean
        upperBound = mean + distanceFromMean
        return np.linspace(lowerBound, upperBound, numberOfValues)