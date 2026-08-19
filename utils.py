import numpy as np
from matplotlib import pyplot as plt
#The Hodgkin-Huxley model provided to solve_ivp
def model(t, y0, I_hold, g_NaT, g_NaP, g_CaT, g_CaH, g_KDR, g_KM, g_L, g_H, p, Vm_NaT, Vm_NaP, Vm_CaT, Vm_CaH, Vm_KDR, Vm_KM, Vm_H, Vh_NaT, Vh_CaT, Vh_CaH, Vh_KDR, Vn_H, km_NaT, km_NaP, km_CaT, km_CaH, km_KDR, km_KM, km_H, kh_NaT, kh_CaT, kh_CaH, kh_KDR, kn_H, tau_m_CaT, tau_m_CaH, tau_m_KDR, tau_m_KM, tau_m_H, tau_h_CaT, tau_h_CaH, tau_h_KDR, tau_n_H, E_Na, E_Ca, E_K, E_L, E_H, C, k_d, A, d, gamma, Ca_cr, g_SK, k_SK, B_c, F, I_app, voltageRateIncrease, useSK, useH, verbose):
    # Unpack initial conditions
    m_CaT0 = y0[0]
    m_CaH0 = y0[1]
    m_KDR0 = y0[2]
    m_KM0 = y0[3]
    m_H0 = y0[4]
    h_NaT0 = y0[5]
    h_CaT0 = y0[6]
    h_CaH0 = y0[7]
    h_KDR0 = y0[8]
    n_H0 = y0[9]
    V0 = y0[10]
    Ca_c = y0[11]
    # Calculate gating functions not given as an argument
    m_NaT = boltzmann(V0, Vm_NaT, km_NaT)
    m_NaP = boltzmann(V0, Vm_NaP, km_NaP)
    #Calculate inactivation time constant for sodium
    tau_h_NaT = timeConstant(V0)
    #Calculate currents
    I_NaT = I_NaT_get(g_NaT, m_NaT, h_NaT0, V0, E_Na)
    I_NaP = I_NaP_get(g_NaP, m_NaP, V0, E_Na)
    I_CaT = I_CaT_get(g_CaT, m_CaT0, h_CaT0, V0, E_Ca)
    I_CaH = I_CaH_get(g_CaH, m_CaH0, h_CaH0, V0, E_Ca)
    I_KDR = I_KDR_get(g_KDR, m_KDR0, h_KDR0, V0, E_K)
    I_KM = I_KM_get(g_KM, m_KM0, V0, E_K)
    I_L = I_L_get(g_L, V0, E_L)
    if useH:
        I_H = I_H_get(g_H, p, m_H0, n_H0, V0, E_H)
    if useSK:
        I_SK = I_SK_get(g_SK, Ca_c, k_SK, V0, E_K)
    # Calculate calcium
    if useSK:
        dCa_c = ((1 + B_c / k_d) ** -1) * (((-(I_CaH + I_CaT) / (2*A*F*d))) - gamma * (Ca_c))
    else:
        dCa_c = 0
    #Calculate voltage derivative
    if voltageRateIncrease:
        if useH:
            if useSK:
                dV = ((I_app.getCurrent(t) + I_hold - I_NaT - I_NaP - I_CaT - I_CaH - I_KDR - I_KM - I_L - I_H - I_SK)) / C
            else:
                dV = ((I_app.getCurrent(t) + I_hold - I_NaT - I_NaP - I_CaT - I_CaH - I_KDR - I_KM - I_L - I_H)) / C
        else:
            if useSK:
                dV = ((I_app.getCurrent(t) + I_hold - I_NaT - I_NaP - I_CaT - I_CaH - I_KDR - I_KM - I_L - I_SK)) / C
            else:
                dV = ((I_app.getCurrent(t) + I_hold - I_NaT - I_NaP - I_CaT - I_CaH - I_KDR - I_KM - I_L)) / C
    else:
        dV = 0
    #Calculate derivative for gating variables
    dh_NaT = gateDerivative(V0, Vh_NaT, kh_NaT, h_NaT0, tau_h_NaT)
    dm_CaT = gateDerivative(V0, Vm_CaT, km_CaT, m_CaT0, tau_m_CaT)
    dh_CaT = gateDerivative(V0, Vh_CaT, kh_CaT, h_CaT0, tau_h_CaT)
    dm_CaH = gateDerivative(V0, Vm_CaH, km_CaH, m_CaH0, tau_m_CaH)
    dh_CaH = gateDerivative(V0, Vh_CaH, kh_CaH, h_CaH0, tau_h_CaH)
    dm_KDR = gateDerivative(V0, Vm_KDR, km_KDR, m_KDR0, tau_m_KDR)
    dh_KDR = gateDerivative(V0, Vh_KDR, kh_KDR, h_KDR0, tau_h_KDR)
    dm_KM = gateDerivative(V0, Vm_KM, km_KM, m_KM0, tau_m_KM)
    if useH:
        dm_H = gateDerivative(V0, Vm_H, km_H, m_H0, tau_m_H)
        dn_H = gateDerivative(V0, Vn_H, kn_H, n_H0, tau_n_H)
    else:
        dm_H = 0
        dn_H = 0
    #Progress tracking
    if verbose:
        print("t " + str(t) + " I " + str(I_app.getCurrent(t)) + " Last V " + str(V0) + " Last C " + str(Ca_c) + " dC " + str(dCa_c))
    # Pack output for solver
    y = np.array([dm_CaT, dm_CaH, dm_KDR, dm_KM, dm_H, dh_NaT, dh_CaT, dh_CaH, dh_KDR, dn_H, dV, dCa_c]).T
    return y
#Gating variables
def gateDerivative(V, Vx, kx, x, tau):
    return (boltzmann(V, Vx, kx) - x) / tau
#Gating variables in boltzman form
def boltzmann(V, Vx, kx):
    return 1 / (1 + np.exp(-(V - Vx) / kx))
#Transient sodium
def I_NaT_get(g_NaT, m_NaT, h_NaT0, V0, E_Na):
    return g_NaT * m_NaT**3 * h_NaT0 * (V0 - E_Na)
#Persistent sodium
def I_NaP_get(g_NaP, m_NaP, V0, E_Na):
    return g_NaP * m_NaP * (V0 - E_Na)
#Transient calcium
def I_CaT_get(g_CaT, m_CaT0, h_CaT0, V0, E_Ca):
    return g_CaT * m_CaT0**2 * h_CaT0 * (V0 - E_Ca)
#High-voltage calcium
def I_CaH_get(g_CaH, m_CaH0, h_CaH0, V0, E_Ca):
    return g_CaH * m_CaH0**2 * h_CaH0 * (V0 - E_Ca)
#Delayed rectifier
def I_KDR_get(g_KDR, m_KDR0, h_KDR0, V0, E_K):
    return g_KDR * m_KDR0 * h_KDR0 * (V0 - E_K)
#M-type potassium
def I_KM_get(g_KM, m_KM0, V0, E_K):
    return g_KM * m_KM0 * (V0 - E_K)
#Leak channel
def I_L_get(g_L, V0, E_L):
    return g_L * (V0 - E_L)
#HCN channel
def I_H_get(g_H, p, m_H0, n_H0, V0, E_H):
    return g_H * (p * m_H0 + (1 - p) * n_H0) * (V0 - E_H)
#SK channel
def I_SK_get(g_SK, Ca_c, k_SK, V0, E_K):
    return g_SK * ((Ca_c ** 5) / ((k_SK ** 5) + (Ca_c ** 5))) * (V0 - E_K)
#Get time constant for sodium inactivation
def timeConstant(V0):
    return 0.2 + 0.007 * (np.exp(np.exp(-(V0 - 40.6)/51.4)))
#Return area of a sphere
def sphereArea(r):
    return 4 * np.pi * r ** 2
#Function used by least square optimizer to approach a target hold voltage, want to minimize returned value (distance between model output and target)
def residuals(x, current, a, b, c, d, e, f, model):
    #Target hold voltage
    target = -80
    vPrime = model.runModel(x[0], current, a, b, c, d, e, f)[10, -1]
    print("Voltage " + str(vPrime) + " , Current " + str(x[0]) + " , Cost " + str(abs(target - vPrime)))
    return (abs(target - vPrime))
#Print the title of each experiment as a seperate plot
def printText(text, saveLocation, saveNumber):
    plt.text(0.5,0.5, text, fontsize=20, horizontalalignment="center", verticalalignment="center", fontstretch="ultra-expanded", wrap=True)
    plt.axis('off')
    plt.savefig(saveLocation + str(saveNumber) + ".1.Experiment Title" + ".png")
    plt.show()