from HodgkinHuxley import HogdkinHuxley

class Tester():
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
        # Conductance
        self.C = None

    def setValues(self):
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
        #Conductance
        self.C = None

    def runTest(self):
        HogdkinHuxley model = HogdkinHuxley()