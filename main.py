from ExperimentManager import ExperimentManager

# They had two sorts of currents, 300 pA, 500 ms and -100 pA, 500 ms, Current from other paper 20 μA/cm2
#Toscana did 0.35 for steady state
# x0 = -5.614e+02
# bounds = [-3e-7 / sphereArea(5e-8), 3e-7 / sphereArea(5e-8)]
# result = least_squares(residuals, x0, bounds=bounds, args=[current, True, False, False])
# print(result)
#
# #Run steady state

if __name__ == '__main__':
#Paper from https://research-information.bris.ac.uk/ws/portalfiles/portal/3018849/pyr_neur_model_preprint.pdf
    CoolExperiment = ExperimentManager(3)
    # CoolExperiment.run("Optimize")
    CoolExperiment.run("Constant")
    # CoolExperiment.run("Restart")
    # CoolExperiment.run("Step")
    # CoolExperiment.run("Restart")
    # CoolExperiment.run("Chirp")
    # CoolExperiment.run("PermutationTesting2")
    # CoolExperiment.run("PermutationTesting")
    # CoolExperiment.run("Debug")