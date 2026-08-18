from ExperimentManager import ExperimentManager

'''
Implementation of five Hodgkin-Huxley models
1. Nowacki et al., 2010 preprint (https://research-information.bris.ac.uk/ws/portalfiles/portal/3018849/pyr_neur_model_preprint.pdf)
2. Saghafi et al., 2024 with parameters from Nowacki et al., 2010
3. Saghafi et al., 2024 with parameters from a differential evolution algorithm
4. Saghafi et al., 2024 with parameters from Nowacki et al., 2010 with SK channel from Ma et al., 2023 (unfitted)
5. Saghafi et al., 2024 with parameters from Nowacki et al., 2010, modified by Mohammed

To create an experiment use the 'ExperimentalManager' class, which takes three arguments:
1. The current (recommended 1, 2, 3 uA/cm^2)
2. The model (Nowacki, Saghafi, Saghafi_DE, Calcium, Saghafi_M)
3. The filepath to save results

Once the class is instantiated, use the 'run' function to run the experiment.
'run' takes one argument corresponding to the type of experiment to run ('Constant' for a 5s constant current, 'Step' for a 500ms step current and 'Chirp' for a 20s 0-15Hz Zap current.
Additionally, run can take 'PermutationTesting' to run over a changing parameter, PermutationTesting2 to run over two parameters in parallel and Restart to reset values.
'''

if __name__ == '__main__':
#Paper from
    Saghafi = ExperimentManager(3)



    # CoolExperiment.run("Optimize")
    CoolExperiment.run("Constant")
    # CoolExperiment.run("Restart")
    # CoolExperiment.run("Step")
    # CoolExperiment.run("Restart")
    # CoolExperiment.run("Chirp")
    # CoolExperiment.run("PermutationTesting2")
    # CoolExperiment.run("PermutationTesting")
    # CoolExperiment.run("Debug")