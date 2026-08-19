import os

from Electrode import Steady
from HodgkinHuxley import HogdkinHuxley
from utils import printText
'''
Used to run multiple simulations in parallel, permuting over two sets of values.
Args:
1. Hold value
2. Max current
3. Indentifier for each value pair
4. First value
5. Second value
Currently set to permute over g_SK and k_SK, can be modified.
'''
def permute(starting_I_hold, peakCurrent, plotNumber, firstValue, secondValue, modelType2):
    saveLocation = "./CalciumParameterSearch/"
    # Make output folder if necessary
    if not os.path.exists(saveLocation):
        os.makedirs(saveLocation)
    # Get model type
    modelType = "Nowacki"
    match modelType2:
        case 0:
            modelType = "Nowacki"
        case 1:
            modelType = "Saghafi"
        case 2:
            modelType = "Saghafi_DE"
        case 3:
            modelType = "Calcium"
        case 4:
            modelType = "Saghafi_M"
    # Determine what channels to use according to model type
    useSK = True
    useH = True
    match modelType:
        case "Nowacki":
            useSK = False
            useH = False
        case "Saghafi":
            useSK = False
            useH = True
        case "Saghafi_DE":
            useSK = False
            useH = True
        case "Calcium":
            useSK = True
            useH = True
        case "Saghafi_M":
            useSK = False
            useH = True
    print("g_SK " + str(firstValue) + ", k_SK " + str(secondValue))
    #Create model
    neuron = HogdkinHuxley()
    neuron.setValues_alt(modelType)
    I_hold = starting_I_hold
    # Update values for this permutation
    neuron.g_SK = firstValue
    neuron.k_SK = secondValue
    # Run to steady state
    current = Steady(0, 30000)
    neuron.runModel(I_hold, current, True, useSK, useH, False, True, False)
    # Run with constant current
    current = Steady(peakCurrent, 5000)
    neuron.runModel(I_hold, current, True, useSK, useH, True, True, False)
    #Print results
    # neuron.prepareToPlot()
    # neuron.plotVoltageTimeSeries(saveLocation, plotNumber, False, True, "Varying g_SK " + str(firstValue) + ", varying k_SK " + str(secondValue))
    # print("Ploting preparation")
    neuron.prepareToPlot()
    # print("Printing title")
    printText("Constant Current " + str(peakCurrent * 100) + "pA, " + "Varying g_SK " + str(firstValue) + ", varying k_SK " + str(secondValue), saveLocation, plotNumber)
    # print("Printing voltage time series")
    neuron.plotVoltageTimeSeries(saveLocation, plotNumber)
    # print("Printing applied current time series")
    neuron.plotAppliedCurrentTimeSeries(saveLocation, plotNumber)
    # print("Printing gating variable time series")
    neuron.plotChannelTimeSeries(saveLocation, plotNumber)
    # print("Printing channel current time series")
    neuron.plotChannelCurrentsTimeSeries(saveLocation, plotNumber)
    # print("Printing calcium concentration time series")
    neuron.plotCalciumConcentration(saveLocation, plotNumber)
    # print("Printing combined calcium current time series")
    neuron.plotCalciumCurrent(saveLocation, plotNumber)