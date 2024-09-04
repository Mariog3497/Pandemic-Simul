import unittest
import numpy as np
from utils import *

class TestSimulationFunctions(unittest.TestCase):
    """
    Unit tests for the simulation functions 'update_infection_rate' and 'calculate_new_infections_deads'.
    """

    def setUp(self):
        """
        Setup method to initialize the configuration before each test.
        """
        self.config = {
            'INFECTIVITY_TIME': 5,  # Example infectivity time in days
            'N_INFECTED_POP': 4,  # Initial number of infected people
            'MORTALITY_RATE': 0.07,  # Mortality rate
            'TOTAL_POP': 1000  # Total population
        }
    
    def test_update_infection_rate_during_transition(self):
        """
        Test 'update_infection_rate' when masks are being implemented during the transition period.
        The test verifies that R0 is adjusted correctly during the transition.
        """
        initial_R0 = 3.0
        final_R0 = 1.1
        day = 10  # Day when mask usage starts
        time_t = 12  # A day during the transition
        delta_R0 = (final_R0 - initial_R0) / 5  # Gradual change in R0 over 5 days

        # Call the function to get the updated infection rate
        infection_rate = update_infection_rate(self.config, initial_R0, final_R0, delta_R0, day, time_t)

        # Manually calculate the expected infection rate
        expected_R0 = max(final_R0, initial_R0 + delta_R0 * (time_t - day))
        expected_infection_rate = np.log(expected_R0) / self.config['INFECTIVITY_TIME']

        # Assert that the calculated infection rate matches the expected rate
        self.assertAlmostEqual(infection_rate, expected_infection_rate, places=5)

    def test_update_infection_rate_after_transition(self):
        """
        Test 'update_infection_rate' after the transition period has completed.
        This test checks that R0 reaches its final value after the transition.
        """
        initial_R0 = 3.0
        final_R0 = 1.1
        day = 10  # Day when mask usage starts
        time_t = 20  # A day after the transition period
        delta_R0 = (final_R0 - initial_R0) / 5  # Change in R0 over 5 days

        # Call the function to get the updated infection rate
        infection_rate = update_infection_rate(self.config, initial_R0, final_R0, delta_R0, day, time_t)

        # After the transition, R0 should have reached the final value
        expected_infection_rate = np.log(final_R0) / self.config['INFECTIVITY_TIME']

        # Assert that the infection rate is the final value
        self.assertAlmostEqual(infection_rate, expected_infection_rate, places=5)
    
    def test_calculate_new_infections_within_population_limit(self):
        """
        Test 'calculate_new_infections_deads' to check if new infections and deaths
        are correctly calculated when the population limit has not been reached.
        """
        ls_infections = [10, 20, 30]  # Previous infections over the days
        time_t = 3
        infection_rate = np.log(3.0) / self.config['INFECTIVITY_TIME']  # Example infection rate

        # Call the function to calculate new infections and deaths
        new_infections, new_deaths = calculate_new_infections_deads(self.config, infection_rate, time_t, ls_infections)

        # Expected new infections and deaths
        expected_new_infections = int(self.config['N_INFECTED_POP'] * np.exp(infection_rate * time_t))
        
        # Verifica si 'time_t' es suficiente para calcular las muertes
        if time_t >= self.config['INFECTIVITY_TIME']:
            expected_new_deaths = int(self.config['MORTALITY_RATE'] * ls_infections[time_t - self.config['INFECTIVITY_TIME']])
        else:
            expected_new_deaths = 0  # No deaths if infectivity time has not been reached

        # Assert that new infections and deaths are correct
        self.assertEqual(new_infections, expected_new_infections)
        self.assertEqual(new_deaths, expected_new_deaths)

    def test_no_deaths_before_infectivity_time(self):
        """
        Test 'calculate_new_infections_deads' to ensure no deaths are calculated
        if the infectivity time has not yet been reached.
        """
        ls_infections = [10]  # Only one day of data
        time_t = 1
        infection_rate = np.log(3.0) / self.config['INFECTIVITY_TIME']  # Example infection rate

        # Call the function to calculate new infections and deaths
        new_infections, new_deaths = calculate_new_infections_deads(self.config, infection_rate, time_t, ls_infections)

        # Expected new infections and no deaths (since infectivity time is not reached)
        expected_new_infections = int(self.config['N_INFECTED_POP'] * np.exp(infection_rate * time_t))
        expected_new_deaths = 0  # No deaths since the infectivity period has not been reached

        # Assert the new infections and deaths are as expected
        self.assertEqual(new_infections, expected_new_infections)
        self.assertEqual(new_deaths, expected_new_deaths)

if __name__ == '__main__':
    unittest.main()
