from Electrode import Steady
from HodgkinHuxley import HogdkinHuxley
from utils import printText


def permute(starting_I_hold, peakCurrent, plotNumber, firstValue, secondValue):
    saveLocation = "./CalciumParameterSearch/"
    print("g_SK " + str(firstValue) + ", k_SK " + str(secondValue))
    neuron = HogdkinHuxley()
    neuron.setValues_alt()
    I_hold = starting_I_hold
    # Update the values
    neuron.g_SK = firstValue
    neuron.k_SK = secondValue
    # Get rid of transient
    current = Steady(0, 1000)
    neuron.runModel(I_hold, current, True, True, False, True, False)
    # Run model
    current = Steady(peakCurrent, 500 * 10)
    neuron.runModel(I_hold, current, True, True, True, True, False)
    neuron.prepareToPlot()
    neuron.plotVoltageTimeSeries(saveLocation, plotNumber, False, True, "Varying g_SK " + str(firstValue) + ", varying k_SK " + str(secondValue))
    print("Ploting preparation")
    neuron.prepareToPlot()
    print("Printing title")
    printText("Constant Current " + str(peakCurrent * 100) + "pA, " + "Varying g_SK " + str(firstValue) + ", varying k_SK " + str(secondValue), saveLocation, plotNumber)
    print("Printing voltage time series")
    neuron.plotVoltageTimeSeries(saveLocation, plotNumber)
    print("Printing applied current time series")
    neuron.plotAppliedCurrentTimeSeries(saveLocation, plotNumber)
    print("Printing gating variable time series")
    neuron.plotChannelTimeSeries(saveLocation, plotNumber)
    print("Printing channel current time series")
    neuron.plotChannelCurrentsTimeSeries(saveLocation, plotNumber)
    print("Printing calcium concentration time series")
    neuron.plotCalciumConcentration(saveLocation, plotNumber)
    print("Printing combined calcium current time series")
    neuron.plotCalciumCurrent(saveLocation, plotNumber)

    # # Calcium
    # self.k_d = 0.1  # um
    # self.A = 3000  # um^2
    # self.d = 0.1  # um
    # self.gamma = 0.01  # ms-1
    # self.Ca_cr = 0.07  # um
    # self.g_SK = 10  # * 1500# nS
    # self.k_SK = 0.8  # uM
    # self.B_c = 90  # microMolar
    # self.Ca_c0 = self.Ca_cr
    # self.F = constants.physical_constants['Faraday constant'][0] * 1e-6  # C mol^-1 converted to smaller version from paper