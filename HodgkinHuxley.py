from cProfile import label

import numpy as np
from scipy.integrate import solve_ivp
from scipy import constants
from matplotlib import pyplot as plt
from utils import model, boltzmann, I_NaT_get, I_NaP_get, I_CaT_get, I_CaH_get, I_KDR_get, \
    I_KM_get, I_L_get, I_H_get, I_SK_get, conversionFactor_mToU, conversionFactor_nToM


class HogdkinHuxley:
    def __init__(self):
        # Initialize conductance
        self.g_NaT = None
        self.g_NaP = None
        self.g_CaT = None
        self.g_CaH = None
        self.g_KDR = None
        self.g_KM = None
        self.g_L = None
        self.g_H = None
        self.g_NaT_alt = None
        self.g_NaP_alt = None
        self.g_CaT_alt = None
        self.g_CaH_alt = None
        self.g_KDR_alt = None
        self.g_KM_alt = None
        self.g_L_alt = None
        self.g_H_alt = None
        # Initialize gating variable
        self.m_NaT_inf = None
        self.m_NaP_inf = None
        self.m_CaT0 = None
        self.m_CaH0 = None
        self.m_KDR0 = None
        self.m_KM0 = None
        self.m_H0 = None
        self.h_NaT0 = None
        self.h_CaT0 = None
        self.h_CaH0 = None
        self.h_KDR0 = None
        self.n_H0 = None
        self.p = None
        # Half activation voltage
        self.Vm_NaT = None
        self.Vm_NaT_alt = None
        self.Vm_NaP = None
        self.Vm_CaT = None
        self.Vm_CaH = None
        self.Vm_KDR = None
        self.Vm_KM = None
        self.Vm_H = None
        self.Vh_NaT = None
        self.Vh_CaT = None
        self.Vh_CaH = None
        self.Vh_KDR = None
        self.Vn_H = None
        # Boltzman constants
        self.km_NaT = None
        self.km_NaP = None
        self.km_CaT = None
        self.km_CaH = None
        self.km_KDR = None
        self.km_KM = None
        self.km_H = None
        self.kh_NaT = None
        self.kh_CaT = None
        self.kh_CaH = None
        self.kh_KDR = None
        self.kn_H = None
        # Initialize time constant
        self.tau_m_CaT = None
        self.tau_m_CaH = None
        self.tau_m_KDR = None
        self.tau_m_KM = None
        self.tau_m_H = None
        self.tau_h_NaT = None
        self.tau_h_CaT = None
        self.tau_h_CaH = None
        self.tau_h_KDR = None
        self.tau_n_H = None
        # Reverse potential
        self.E_Na = None
        self.E_Ca = None
        self.E_K = None
        self.E_L = None
        self.E_H = None
        # Membrane voltage
        self.V0 = None
        # Conductance
        self.C = None
        #Holding current
        self.I_hold = None
        #Time series data
        self.t_m_NaT = np.array([])
        self.t_m_NaP = np.array([])
        self.t_m_CaT = np.array([])
        self.t_m_CaH = np.array([])
        self.t_m_KDR = np.array([])
        self.t_m_KM = np.array([])
        self.t_m_H = np.array([])
        self.t_h_NaT = np.array([])
        self.t_h_CaT = np.array([])
        self.t_h_CaH = np.array([])
        self.t_h_KDR = np.array([])
        self.t_n_H = np.array([])
        self.t_V = np.array([])
        self.t_I_app = np.array([])
        self.t_eval = np.array([])
        self.t_m_NaT = np.array([])
        self.t_m_NaP = np.array([])
        self.t_I_NaT = np.array([])
        self.t_I_NaP = np.array([])
        self.t_I_CaT = np.array([])
        self.t_I_CaH = np.array([])
        self.t_I_KDR = np.array([])
        self.t_I_KM = np.array([])
        self.t_I_L = np.array([])
        self.t_I_H = np.array([])
        self.length_tracker = np.array([])
        self.final_t_eval = np.array([])
        # Calcium
        self.k_d = None
        self.A = None
        self.d = None
        self.gamma = None
        self.Ca_cr = None
        self.g_SK = None
        self.k_SK = None
        self.B_c = None
        self.F = None
        # Calcium time series
        self.t_Ca = np.array([])
        self.t_I_SK = np.array([])

    def setValues(self):
        #Units
        # Initialize conductance
        self.g_NaT = 65.0
        self.g_NaP = 0.1
        self.g_CaT = 0.6
        self.g_CaH = 0.74
        self.g_KDR = 9.5
        self.g_KM = 0.8
        self.g_L = 0.02
        self.g_H = 0.05
        # Initialize gating variable
        self.m_CaT0 = 0.005499631115330787
        self.m_CaH0 = 2.2658458242948663e-06
        self.m_KDR0 = 0.0014881270089334075
        self.m_KM0 = 0.0067010649216514805
        self.m_H0 = 0.15534913916228063
        self.h_NaT0 = 0.6709528877756887
        self.h_CaT0 = 0.8536179164156359
        self.h_CaH0 = 0.9455957087204464
        self.h_KDR0 = 0.7721798208565878
        self.n_H0 = 0.024873681844352076
        # Half activation voltage
        self.Vm_NaT = -37
        self.setValues_Repeats()

    def setValues_alt(self):
        #Units
        # Initialize conductance
        self.g_NaT = 7.2603
        self.g_NaP = 0.0423
        self.g_CaT = 0.067
        self.g_CaH = 1.5208
        self.g_KDR = 12.505
        self.g_KM = 3.3837
        self.g_L = 0.0035
        self.g_H = 0.0503
        # Initialize gating variable
        self.m_CaT0 = 0.005486594704365255
        self.m_CaH0 = 2.260443363987366e-06
        self.m_KDR0 = 0.0014881270089334075
        self.m_KM0 = 0.006693236665689997
        self.m_H0 = 0.1554691454071592
        self.h_NaT0 = 0.6713104329954209
        self.h_CaT0 = 0.8537921873675318
        self.h_CaH0 = 0.9456737145278049
        self.h_KDR0 = 0.7694232333411584
        self.n_H0 = 0.024919369791676596
        # Half activation voltage
        self.Vm_NaT = -60
        self.setValues_Repeats()

    def setValues_Repeats(self):
        # Initialize gating variable
        self.m_NaT_inf = 0
        self.m_NaP_inf = 0
        self.p = 0.85
        # Half activation voltage
        self.Vm_NaP = -47
        self.Vm_CaT = -54
        self.Vm_CaH = -15
        self.Vm_KDR = -5.8
        self.Vm_KM = -30
        self.Vm_H = -102
        self.Vh_NaT = -75
        self.Vh_CaT = -65
        self.Vh_CaH = -60
        self.Vh_KDR = -68
        self.Vn_H = -102
        # Boltzman constants
        self.km_NaT = 5
        self.km_NaP = 3
        self.km_CaT = 5
        self.km_CaH = 5
        self.km_KDR = 11.4
        self.km_KM = 10
        self.km_H = -13
        self.kh_NaT = -7
        self.kh_CaT = -8.5
        self.kh_CaH = -7
        self.kh_KDR = -9.7
        self.kn_H = -6
        # Initialize time constant
        self.tau_m_CaT = 2
        self.tau_m_CaH = 0.08
        self.tau_m_KDR = 1
        self.tau_m_KM = 75
        self.tau_m_H = 15
        self.tau_h_CaT = 32
        self.tau_h_CaH = 300
        self.tau_h_KDR = 1400
        self.tau_n_H = 210
        # Reverse potential
        self.E_Na = 60
        self.E_Ca = 90
        self.E_K = -85
        self.E_L = -65
        self.E_H = -30
        # Membrane voltage
        self.V0 = -80
        # Conductance
        self.C = 1
        # Calcium
        self.k_d = 0.1  # um
        self.A = 3000  # um^2
        self.d = 0.1  # um
        self.gamma = 0.01  # ms-1
        self.Ca_cr = 0.07  # um
        self.g_SK = 10  #* 1500# nS
        # self.k_SK = 0.73  # uM
        self.k_SK = 0.8  # uM
        self.B_c = 90  # microMolar
        self.Ca_c0 = self.Ca_cr
        self.F = constants.physical_constants['Faraday constant'][0] * 1e-6  # C mol^-1 converted to smaller version from paper

    def updateValues(self, m_CaT0, m_CaH0, m_KDR0, m_KM0, m_H0, h_NaT0, h_CaT0, h_CaH0, h_KDR0, n_H0):
        self.m_CaT0 = m_CaT0
        self.m_CaH0 = m_CaH0
        self.m_KDR0 = m_KDR0
        self.m_KM0 = m_KM0
        self.m_H0 = m_H0
        self.h_NaT0 = h_NaT0
        self.h_CaT0 = h_CaT0
        self.h_CaH0 = h_CaH0
        self.h_KDR0 = h_KDR0
        self.n_H0 = n_H0

    def runModel(self, I_hold, I_app, voltageRateIncrease, useSK, memory, updateStart, verbose, stepSize = 0.01):
        # Prepare ODE run
        start = 0
        self.step = stepSize
        self.length = I_app.getLength()
        t_span = [0, self.length]
        self.t_eval = np.arange(start, self.length, self.step)
        self.I_hold = I_hold
        y0_Gates = np.array([self.m_CaT0, self.m_CaH0, self.m_KDR0, self.m_KM0, self.m_H0, self.h_NaT0, self.h_CaT0, self.h_CaH0, self.h_KDR0, self.n_H0, self.V0, self.Ca_c0]).T
        args =[self.I_hold, self.g_NaT, self.g_NaP, self.g_CaT, self.g_CaH, self.g_KDR, self.g_KM, self.g_L, self.g_H, self.p, self.Vm_NaT, self.Vm_NaP, self.Vm_CaT, self.Vm_CaH, self.Vm_KDR, self.Vm_KM, self.Vm_H, self.Vh_NaT, self.Vh_CaT, self.Vh_CaH, self.Vh_KDR, self.Vn_H, self.km_NaT, self.km_NaP, self.km_CaT, self.km_CaH, self.km_KDR, self.km_KM, self.km_H, self.kh_NaT, self.kh_CaT, self.kh_CaH, self.kh_KDR, self.kn_H, self.tau_m_CaT, self.tau_m_CaH, self.tau_m_KDR, self.tau_m_KM, self.tau_m_H, self.tau_h_CaT, self.tau_h_CaH, self.tau_h_KDR, self.tau_n_H, self.E_Na, self.E_Ca, self.E_K, self.E_L, self.E_H, self.C, self.k_d, self.A, self.d, self.gamma, self.Ca_cr, self.g_SK, self.k_SK, self.B_c, self.F, I_app, voltageRateIncrease, useSK, verbose]
        # Run ODE for gating  , method="DOP853", rtol=1e-10, atol=1e-13
        ODEresults = solve_ivp(model, t_span, y0_Gates, t_eval=self.t_eval, args=args, method="LSODA", max_step = 0.005, rtol=1e-13, atol=1e-8)
        z = ODEresults.y
        if verbose:
            print(ODEresults.message)
        #Unpack
        if memory: #Save timeseries
            if verbose:
                print("Saving ODE time series")
            #Time series
            self.t_m_CaT = np.append(self.t_m_CaT, z[0])
            self.t_m_CaH = np.append(self.t_m_CaH, z[1])
            self.t_m_KDR = np.append(self.t_m_KDR, z[2])
            self.t_m_KM = np.append(self.t_m_KM, z[3])
            self.t_m_H = np.append(self.t_m_H, z[4])
            self.t_h_NaT = np.append(self.t_h_NaT, z[5])
            self.t_h_CaT = np.append(self.t_h_CaT, z[6])
            self.t_h_CaH = np.append(self.t_h_CaH, z[7])
            self.t_h_KDR = np.append(self.t_h_KDR, z[8])
            self.t_n_H = np.append(self.t_n_H, z[9])
            self.t_V = np.append(self.t_V, z[10])
            self.t_Ca = np.append(self.t_Ca, z[11])
            self.t_I_app = np.append(self.t_I_app, I_app.getMultipleCurrents(self.t_eval))

            if verbose:
                print("Deriving time series")
            for i,voltage in enumerate(z[10]):
                self.t_m_NaT = np.append(self.t_m_NaT, boltzmann(voltage, self.Vm_NaT, self.km_NaT))
                self.t_m_NaP = np.append(self.t_m_NaP, boltzmann(voltage, self.Vm_NaP, self.km_NaP))
                self.t_I_NaT = np.append(self.t_I_NaT, I_NaT_get(self.g_NaT, self.t_m_NaT[i], self.t_h_NaT[i], voltage, self.E_Na))
                self.t_I_NaP = np.append(self.t_I_NaP, I_NaP_get(self.g_NaP, self.t_m_NaP[i], voltage, self.E_Na))
                self.t_I_CaT = np.append(self.t_I_CaT, I_CaT_get(self.g_CaT, self.t_m_CaT[i], self.t_h_CaT[i], voltage, self.E_Ca))
                self.t_I_CaH = np.append(self.t_I_CaH, I_CaH_get(self.g_CaH, self.t_m_CaH[i], self.t_h_CaH[i], voltage, self.E_Ca))
                self.t_I_KDR = np.append(self.t_I_KDR, I_KDR_get(self.g_KDR, self.t_m_KDR[i], self.t_h_KDR[i], voltage, self.E_K))
                self.t_I_KM = np.append(self.t_I_KM, I_KM_get(self.g_KM, self.t_m_KM[i], voltage, self.E_K))
                self.t_I_L = np.append(self.t_I_L, I_L_get(self.g_L, voltage, self.E_L))
                self.t_I_H = np.append(self.t_I_H, I_H_get(self.g_H, self.p, self.t_m_H[i], self.t_n_H[i], voltage, self.E_H))
                self.t_I_SK = np.append(self.t_I_SK, I_SK_get(self.g_SK, self.t_Ca[i], self.k_SK, voltage, self.E_K))
            # print(I_app.getCurrent(I_app.getLength))
            # print(I_hold)
            # print(self.t_I_NaT[-1] + self.t_I_NaP[-1] + self.t_I_CaT[-1] + self.t_I_CaH[-1] + self.t_I_KDR[-1] + self.t_I_KM[-1] + self.t_I_L[-1] + self.t_I_H[-1])
            # print("t_I_NaT " + str(self.t_I_NaT[-1]))
            # print("t_I_NaP " + str(self.t_I_NaP[-1]))
            # print("t_I_CaT " + str(self.t_I_CaT[-1]))
            # print("t_I_CaH " + str(self.t_I_CaH[-1]))
            # print("t_I_KDR " + str(self.t_I_KDR[-1]))
            # print("t_I_KM " + str(self.t_I_KM[-1]))
            # print("t_I_L " + str(self.t_I_L[-1]))
            # print("t_I_H " + str(self.t_I_H[-1]))
            # print("hCaT " + str(self.t_h_CaT[-1]))
            # print("hCaT_INF " + str(boltzmann(z[10][-1], self.Vh_CaT, self.kh_CaT)))
            # print("t_I_SK " + str(self.t_I_SK[-1]))

            #Deal with t_eval
            self.length_tracker = np.append(self.length_tracker,self.length)

        if updateStart:
            if verbose:
                print("Updating starting conditions")
            #New initial conditions
            self.m_CaT0 = z[0, -1]
            self.m_CaH0 = z[1, -1]
            self.m_KDR0 = z[2, -1]
            self.m_KM0 = z[3, -1]
            self.m_H0 = z[4, -1]
            self.h_NaT0 = z[5, -1]
            self.h_CaT0 = z[6, -1]
            self.h_CaH0 = z[7, -1]
            self.h_KDR0 = z[8, -1]
            self.n_H0 = z[9, -1]
            self.V0 = z[10, -1]
            self.Ca_c0 = z[11, -1]
        return z

    def plotVoltageTimeSeries(self, saveLocation, saveNumber, save = True, show = True, additionalText=""):
        plt.plot(self.final_t_eval, self.t_V)
        plt.xlabel("Time (ms)")
        plt.ylabel("mV")
        if additionalText != "":
            additionalText = " " + additionalText
        plt.title("Voltage Trace" + additionalText)
        if save:
            plt.savefig(saveLocation + str(saveNumber) + ".2.Voltage Trace" + ".png")
        if show:
            plt.show()

    def plotAppliedCurrentTimeSeries(self, saveLocation, saveNumber):
        plt.plot(self.final_t_eval, self.t_I_app)
        plt.xlabel("Time (ms)")
        plt.ylabel("Current (mA/cm^2)")
        plt.title("Applied Current")
        plt.savefig(saveLocation + str(saveNumber) + ".3.Applied Current Timeseries" + ".png")
        plt.show()

    def plotChannelTimeSeries(self, saveLocation, saveNumber):
        plt.plot(self.final_t_eval, self.t_m_NaT, label="mNaT")
        plt.plot(self.final_t_eval, self.t_m_NaP, label="mNaP")
        plt.plot(self.final_t_eval, self.t_m_CaT, label="mCaT")
        plt.plot(self.final_t_eval, self.t_m_CaH, label="mCaH")
        plt.plot(self.final_t_eval, self.t_m_KDR, label="mKDR")
        plt.plot(self.final_t_eval, self.t_m_KM, label="mKM")
        plt.plot(self.final_t_eval, self.t_h_NaT, label="hNaT")
        plt.plot(self.final_t_eval, self.t_h_CaT, label="hCaT")
        plt.plot(self.final_t_eval, self.t_h_CaH, label="hCaH")
        plt.plot(self.final_t_eval, self.t_h_KDR, label="hKDR")
        plt.plot(self.final_t_eval, self.t_n_H, label="nH")
        plt.xlabel("Time (ms)")
        plt.ylabel("Gating variables")
        plt.title("Gating Variables")
        plt.legend(loc="upper right")
        plt.savefig(saveLocation + str(saveNumber) + ".4.Gating Variable Timeseries" + ".png")
        plt.show()

    def plotChannelCurrentsTimeSeries(self, saveLocation, saveNumber):
        plt.plot(self.final_t_eval, self.t_I_NaT, label="NaT")
        plt.plot(self.final_t_eval, self.t_I_NaP, label="NaP")
        plt.plot(self.final_t_eval, self.t_I_CaT, label="CaT")
        plt.plot(self.final_t_eval, self.t_I_CaH, label="CaH")
        plt.plot(self.final_t_eval, self.t_I_KDR, label="KDR")
        plt.plot(self.final_t_eval, self.t_I_KM, label="KM")
        plt.plot(self.final_t_eval, self.t_I_L, label="L")
        plt.plot(self.final_t_eval, self.t_I_H, label="H")
        plt.plot(self.final_t_eval, self.t_I_SK, label="SK")
        plt.xlabel("Time (ms)")
        plt.ylabel("Current (nA/cm^2)")
        plt.legend(loc="upper right")
        plt.title("Channel Currents")
        plt.savefig(saveLocation + str(saveNumber) + ".5.Channel Current Timeseries" + ".png")
        plt.show()

    def plotCalciumCurrent(self, saveLocation, saveNumber):
        plt.plot(self.final_t_eval, self.t_I_CaT + self.t_I_CaH, label="I_Ca")
        plt.xlabel("Time (ms)")
        plt.ylabel("Current (nA/cm^2)")
        plt.legend(loc="upper right")
        plt.title("ICa")
        plt.savefig(saveLocation + str(saveNumber) + ".6.Combined Ca Current Timeseries" + ".png")
        plt.show()

    def plotCalciumConcentration(self, saveLocation, saveNumber):
        plt.plot(self.final_t_eval, self.t_Ca)
        plt.xlabel("Time (ms)")
        plt.ylabel("[Ca] (uM)")
        plt.title("Calcium Concentration")
        plt.savefig(saveLocation + str(saveNumber) + ".7.Calcium Concentration" + ".png")
        plt.show()

    def prepareToPlot(self):
        self.final_t_eval = np.arange(0, self.length_tracker.sum(), self.step)