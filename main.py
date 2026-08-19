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

    # Nowacki_1 = ExperimentManager(1, "Nowacki", "./Runs/Nowacki/Step/100uA/")
    # Nowacki_1.run("Step")
    # Nowacki_2 = ExperimentManager(2, "Nowacki", "./Runs/Nowacki/Step/200uA/")
    # Nowacki_2.run("Step")
    # Nowacki_3 = ExperimentManager(3, "Nowacki", "./Runs/Nowacki/Step/300uA/")
    # Nowacki_3.run("Step")
    # Nowacki_1 = ExperimentManager(1, "Nowacki", "./Runs/Nowacki/Constant/100uA/")
    # Nowacki_1.run("Constant")
    # Nowacki_2 = ExperimentManager(2, "Nowacki", "./Runs/Nowacki/Constant/200uA/")
    # Nowacki_2.run("Constant")
    # Nowacki_3 = ExperimentManager(3, "Nowacki", "./Runs/Nowacki/Constant/300uA/")
    # Nowacki_3.run("Constant")
    # Nowacki_1 = ExperimentManager(1, "Nowacki", "./Runs/Nowacki/Chirp/100uA/")
    # Nowacki_1.run("Chirp")
    # Nowacki_2 = ExperimentManager(2, "Nowacki", "./Runs/Nowacki/Chirp/200uA/")
    # Nowacki_2.run("Chirp")
    # Nowacki_3 = ExperimentManager(3, "Nowacki", "./Runs/Nowacki/Chirp/300uA/")
    # Nowacki_3.run("Chirp")
    # Saghafi_1 = ExperimentManager(1, "Saghafi", "./Runs/Step/Saghafi/100uA/")
    # Saghafi_1.run("Step")
    # Saghafi_2 = ExperimentManager(2, "Saghafi", "./Runs/Step/Saghafi/200uA/")
    # Saghafi_2.run("Step")
    # Saghafi_3 = ExperimentManager(3, "Saghafi", "./Runs/Step/Saghafi/300uA/")
    # Saghafi_3.run("Step")
    #
    # Saghafi_DE_1 = ExperimentManager(1, "Saghafi_DE", "./Runs/Step/Saghafi_DE/100uA/")
    # Saghafi_DE_1.run("Step")
    # Saghafi_DE_2 = ExperimentManager(2, "Saghafi_DE", "./Runs/Step/Saghafi_DE/200uA/")
    # Saghafi_DE_2.run("Step")
    # Saghafi_DE_3 = ExperimentManager(3, "Saghafi_DE", "./Runs/Step/Saghafi_DE/300uA/")
    # Saghafi_DE_3.run("Step")
    # Saghafi_DE_1 = ExperimentManager(1, "Saghafi_DE", "./Runs/Constant/Saghafi_DE/100uA/")
    # Saghafi_DE_1.run("Constant")
    # Saghafi_DE_2 = ExperimentManager(2, "Saghafi_DE", "./Runs/Constant/Saghafi_DE/200uA/")
    # Saghafi_DE_2.run("Constant")
    # Saghafi_DE_3 = ExperimentManager(3, "Saghafi_DE", "./Runs/Constant/Saghafi_DE/300uA/")
    # Saghafi_DE_3.run("Constant")
    # Saghafi_DE_1 = ExperimentManager(1, "Saghafi_DE", "./Runs/Chirp/Saghafi_DE/100uA/")
    # Saghafi_DE_1.run("Chirp")
    # Saghafi_DE_2 = ExperimentManager(2, "Saghafi_DE", "./Runs/Chirp/Saghafi_DE/200uA/")
    # Saghafi_DE_2.run("Chirp")
    # Saghafi_DE_3 = ExperimentManager(3, "Saghafi_DE", "./Runs/Chirp/Saghafi_DE/300uA/")
    # Saghafi_DE_3.run("Chirp")
    #
    # Calcium_1 = ExperimentManager(1, "Calcium", "./Runs/Step/Calcium/100uA/")
    # Calcium_1.run("Step")
    # Calcium_2 = ExperimentManager(2, "Calcium", "./Runs/Step/Calcium/200uA/")
    # Calcium_2.run("Step")
    # Calcium_3 = ExperimentManager(2, "Calcium", "./Runs/Step/Calcium/300uA/")
    # Calcium_3.run("Step")
    # Calcium_1 = ExperimentManager(1, "Calcium", "./Runs/Constant/Calcium/100uA/")
    # Calcium_1.run("Constant")
    # Calcium_2 = ExperimentManager(2, "Calcium", "./Runs/Constant/Calcium/200uA/")
    # Calcium_2.run("Constant")
    # Calcium_3 = ExperimentManager(2, "Calcium", "./Runs/Constant/Calcium/300uA/")
    # Calcium_3.run("Constant")
    # Calcium_1 = ExperimentManager(1, "Calcium", "./Runs/Chirp/Calcium/100uA/")
    # Calcium_1.run("Chirp")
    # Calcium_2 = ExperimentManager(2, "Calcium", "./Runs/Chirp/Calcium/200uA/")
    # Calcium_2.run("Chirp")
    # Calcium_3 = ExperimentManager(2, "Calcium", "./Runs/Chirp/Calcium/300uA/")
    # Calcium_3.run("Chirp")
    #
    # Saghafi_M_1 = ExperimentManager(1, "Saghafi_M", "./Runs/Step/Saghafi_M/100uA/")
    # Saghafi_M_1.run("Step")
    # Saghafi_M_2 = ExperimentManager(2, "Saghafi_M", "./Runs/Step/Saghafi_M/200uA/")
    # Saghafi_M_2.run("Step")
    # Saghafi_M_3 = ExperimentManager(3, "Saghafi_M", "./Runs/Step/Saghafi_M/300uA/")
    # Saghafi_M_3.run("Step")
    # Saghafi_M_1 = ExperimentManager(1, "Saghafi_M", "./Runs/Constant/Saghafi_M/100uA/")
    # Saghafi_M_1.run("Constant")
    # Saghafi_M_2 = ExperimentManager(2, "Saghafi_M", "./Runs/Constant/Saghafi_M/200uA/")
    # Saghafi_M_2.run("Constant")
    # Saghafi_M_3 = ExperimentManager(3, "Saghafi_M", "./Runs/Constant/Saghafi_M/300uA/")
    # Saghafi_M_3.run("Constant")
    # Saghafi_M_1 = ExperimentManager(1, "Saghafi_M", "./Runs/Chirp/Saghafi_M/100uA/")
    # Saghafi_M_1.run("Chirp")
    # Saghafi_M_2 = ExperimentManager(2, "Saghafi_M", "./Runs/Chirp/Saghafi_M/200uA/")
    # Saghafi_M_2.run("Chirp")
    # Saghafi_M_3 = ExperimentManager(3, "Saghafi_M", "./Runs/Chirp/Saghafi_M/300uA/")
    # Saghafi_M_3.run("Chirp")

    Calcium_1 = ExperimentManager(1, "Calcium", "./Runs/PermutationTest/")
    Calcium_1.run("PermutationTesting2")