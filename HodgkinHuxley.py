import numpy as np
from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt
from utils import model


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
        #Time series data
        self.t_m_NaT = None
        self.t_m_NaP = None
        self.t_m_CaT = None
        self.t_m_CaH = None
        self.t_m_KDR = None
        self.t_m_KM = None
        self.t_m_H = None
        self.t_h_NaT = None
        self.t_h_CaT = None
        self.t_h_CaH = None
        self.t_h_KDR = None
        self.t_n_H = None
        self.t_V = None
        self.t_I_app = None
        self.t_eval = None


    def setValues(self):
        # Initialize conductance
        self.g_NaT = 65.0
        self.g_NaP = 0.1
        self.g_CaT = 0.6
        self.g_CaH = 0.74
        self.g_KDR = 9.5
        self.g_KM = 0.8
        self.g_L = 0.02
        self.g_H = 0.05
        self.g_NaT_alt = 7.2603
        self.g_NaP_alt = 0.0423
        self.g_CaT_alt = 0.067
        self.g_CaH_alt = 1.5208
        self.g_KDR_alt = 12.505
        self.g_KM_alt = 3.3837
        self.g_L_alt = 0.0035
        self.g_H_alt = 0.0503
        # Initialize gating variable
        self.m_NaT_inf = 0
        self.m_NaP_inf = 0
        self.m_CaT0 = 0
        self.m_CaH0 = 0
        self.m_KDR0 = 0
        self.m_KM0 = 0
        self.m_H0 = 0
        self.h_NaT0 = 0
        self.h_CaT0 = 0
        self.h_CaH0 = 0
        self.h_KDR0 = 0
        self.n_H0 = 0
        self.p = 0.85
        # Half activation voltage
        self.Vm_NaT = -37
        self.Vm_NaT_alt = -60.0
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

    def runModel(self, I_app):
        # Prepare ODE run
        start = 0
        step = 1
        length = I_app.getLength()
        t_span = [0, length]
        self.t_eval = np.arange(start, length, step)
        y0_Gates = np.array([self.m_NaT_inf, self.m_NaP_inf, self.m_CaT0, self.m_CaH0, self.m_KDR0, self.m_KM0, self.m_H0, self.h_NaT0, self.h_CaT0, self.h_CaH0, self.h_KDR0, self.n_H0, self.V0]).T
        args =[self.g_NaT, self.g_NaP, self.g_CaT, self.g_CaH, self.g_KDR, self.g_KM, self.g_L, self.g_H, self.p, self.Vm_NaT, self.Vm_NaP, self.Vm_CaT, self.Vm_CaH, self.Vm_KDR, self.Vm_KM, self.Vm_H, self.Vh_NaT, self.Vh_CaT, self.Vh_CaH, self.Vh_KDR, self.Vn_H, self.km_NaT, self.km_NaP, self.km_CaT, self.km_CaH, self.km_KDR, self.km_KM, self.km_H, self.kh_NaT, self.kh_CaT, self.kh_CaH, self.kh_KDR, self.kn_H, self.tau_m_CaT, self.tau_m_CaH, self.tau_m_KDR, self.tau_m_KM, self.tau_m_H, self.tau_h_CaT, self.tau_h_CaH, self.tau_h_KDR, self.tau_n_H, self.E_Na, self.E_Ca, self.E_K, self.E_L, self.E_H, self.C, I_app]
        # Run ODE for gating
        z = solve_ivp(model, t_span, y0_Gates, t_eval=self.t_eval, args=args).y
        #Unpack
        #Time series
        self.t_m_NaT = z[0]
        self.t_m_NaP = z[1]
        self.t_m_CaT = z[2]
        self.t_m_CaH = z[3]
        self.t_m_KDR = z[4]
        self.t_m_KM = z[5]
        self.t_m_H = z[6]
        self.t_h_NaT = z[7]
        self.t_h_CaT = z[8]
        self.t_h_CaH = z[9]
        self.t_h_KDR = z[10]
        self.t_n_H = z[11]
        self.t_V = z[12]
        self.t_I_app = I_app.getMultipleCurrents(self.t_eval)
        #New initial conditions
        self.m_NaT_inf = z[0,-1]
        self.m_NaP_inf = z[1, -1]
        self.m_CaT0 = z[2, -1]
        self.m_CaH0 = z[3, -1]
        self.m_KDR0 = z[4, -1]
        self.m_KM0 = z[5, -1]
        self.m_H0 = z[6, -1]
        self.h_NaT0 = z[7, -1]
        self.h_CaT0 = z[8, -1]
        self.h_CaH0 = z[9, -1]
        self.h_KDR0 = z[10, -1]
        self.n_H0 = z[11, -1]
        self.V0 = z[12, -1]

    def plotVoltageTimeSeries(self):
        plt.plot(self.t_eval, self.t_V)
        plt.xlabel("Time (ms)")
        plt.ylabel("V")
        plt.show()