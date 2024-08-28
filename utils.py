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