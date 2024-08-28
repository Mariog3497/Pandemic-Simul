import numpy as np
import pandas as pd

def update_infection_rate(config, initial_R0, final_R0, delta_R0, day, time_t):
    """
    This function gradually adjusts the infection rate considering the adaptation period 
    to events such as wearing masks or vaccination.
       
    Parameters:
        config (dict): Configuration dictionary containing global variables.
        initial_R0 (float): Initial reproduction number (R0) before the event.
        final_R0 (float): Final reproduction number (R0) after the event is fully implemented.
        delta_R0 (float): Daily change in R0 during the transition period.
        day (int): Day when the event starts.
        time_t (int): Current day of the simulation.
            
    Returns:
        float: Updated infection rate at time t.
    """
    # Extract global variables from the config dictionary
    INFECTIVITY_TIME = config['INFECTIVITY_TIME']
    
    # Gradually adjust the R0 value
    current_R0 = max(final_R0, initial_R0 + delta_R0 * (time_t - day))
    
    # Calculate the infection rate as the logarithm of R0 divided by infectivity time
    infection_rate = np.log(current_R0) / INFECTIVITY_TIME
    
    return infection_rate

def calculate_new_infections_deads(config, infection_rate, time_t, ls_infections):
    """
    Calculate the new infections and deaths for a given day in the simulation.
    
    Parameters:
        config (dict): Configuration dictionary containing global variables.
        infection_rate (float): The current infection rate at day time_t.
        time_t (int): The current day in the simulation.
        ls_infections (list): A list of the number of infections per day up to time_t.
        
    Returns:
        tuple: A tuple containing the number of new infections and new deaths for the day t.
    """
    # Extract global variables from the config dictionary
    N_INFECTED_POP = config['N_INFECTED_POP']
    MORTALITY_RATE = config['MORTALITY_RATE']
    INFECTIVITY_TIME = config['INFECTIVITY_TIME']
    TOTAL_POP = config['TOTAL_POP']
    
    # Calculate new infections for the current day
    new_infections = int(N_INFECTED_POP * np.exp(infection_rate * time_t))
    
    # Calculate new deaths for the current day
    if len(ls_infections) > INFECTIVITY_TIME:
        new_deads = int(MORTALITY_RATE * ls_infections[time_t - INFECTIVITY_TIME])
    else:
        new_deads = 0
    
    # Adjust new infections if the total exceeds the population
    if sum(ls_infections) + new_infections >= TOTAL_POP:
        new_infections = TOTAL_POP - sum(ls_infections)
        # Adjust new deads if the total exceeds the population
        new_deads = int(MORTALITY_RATE * ls_infections[time_t - INFECTIVITY_TIME]) if len(ls_infections) > INFECTIVITY_TIME else 0
        if new_deads >= TOTAL_POP:
            new_deads = 0

    return new_infections, new_deads