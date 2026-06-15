import numpy as np
from scipy.integrate import solve_ivp


class HogdkinHuxley:
    def __init__(self, g_NaT, g_NaP, g_CaT, g_CaH, g_KDR, g_KM, g_L, g_H, m_NaT_inf, m_NaP_inf, m_CaT0, m_CaH0, m_KDR0, m_KM0, m_H0, h_NaT0, h_CaT0, h_CaH0, h_KDR0, n_H0, p, tau_m_CaT, tau_m_CaH, tau_m_KDR, tau_m_KM, tau_m_H, tau_h_NaT, tau_h_CaT, tau_h_CaH, tau_h_KDR, tau_n_H, E_Na, E_Ca, E_K, E_L, E_H, C):
        # Initialize currents
        self.I_app = None
        self.I_NaT = None
        self.I_NaP = None
        self.I_CaT = None
        self.I_CaH = None
        self.I_KDR = None
        self.I_KM = None
        self.I_L = None
        self.I_KH = None
        # Initialize conductance
        self.g_NaT = g_NaT
        self.g_NaP = g_NaP
        self.g_CaT = g_CaT
        self.g_CaH = g_CaH
        self.g_KDR = g_KDR
        self.g_KM = g_KM
        self.g_L = g_L
        self.g_H = g_H
        # Initialize gating variable
        self.m_NaT_inf = m_NaT_inf
        self.m_NaP_inf = m_NaP_inf
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
        self.p = p
        # Initialize time constant
        self.tau_m_CaT = tau_m_CaT
        self.tau_m_CaH = tau_m_CaH
        self.tau_m_KDR = tau_m_KDR
        self.tau_m_KM = tau_m_KM
        self.tau_m_H = tau_m_H
        self.tau_h_NaT = tau_h_NaT
        self.tau_h_CaT = tau_h_CaT
        self.tau_h_CaH = tau_h_CaH
        self.tau_h_KDR = tau_h_KDR
        self.tau_n_H = tau_n_H
        # Reverse potential
        self.E_Na = E_Na
        self.E_Ca = E_Ca
        self.E_K = E_K
        self.E_L = E_L
        self.E_H = E_H
        # Membrane voltage
        self.V = None
        # Conductance
        self.C = C

    def runModel(self, V, length):
        # Prepare ODE run
        start = 0
        step = 1
        t_span = [0, length]
        t_eval = np.arange(start, length, step)
        y0_Gates = np.array(
            [self.m_CaT0, self.m_CaH0, self.m_KDR0, self.m_KM0, self.m_H0, self.h_NaT0, self.h_CaT0, self.h_CaH0,
             self.h_KDR0, self.n_H0]).T
        args_Gates = [V]
        # Run ODE for gating
        z = solve_ivp(self.ODEModelGating, t_span, y0_Gates, t_eval=t_eval, args=args_Gates)
        #Unpack
        # Run ODE for currents
        z = solve_ivp(self.ODEModelCurrent, t_span, V0, t_eval=t_eval, args=)

    def ODEModelGating(self, V):
    # Unpack

    # Deal with currents

    def gatingHelper(self, x_inf, x, tau):
        return (x_inf - x) / tau

    def ODEModelCurrent(self):
        # Unpack

        # Deal with currents