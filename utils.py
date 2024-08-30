import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    # Gradually adjust the R0 value
    current_R0 = max(final_R0, initial_R0 + delta_R0 * (time_t - day))
    
    # Calculate the infection rate as the logarithm of R0 divided by infectivity time
    infection_rate = np.log(current_R0) / config['INFECTIVITY_TIME']
    
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
    # Calculate new infections for the current day
    new_infections = int(config['N_INFECTED_POP'] * np.exp(infection_rate * time_t))
    
    # Calculate new deaths for the current day
    if len(ls_infections) > config['INFECTIVITY_TIME']:
        new_deads = int(config['MORTALITY_RATE'] * ls_infections[time_t - config['INFECTIVITY_TIME']])
    else:
        new_deads = 0
    
    # Adjust new infections if the total exceeds the population
    if sum(ls_infections) + new_infections >= config['TOTAL_POP']:
        new_infections = config['TOTAL_POP'] - sum(ls_infections)
        # Adjust new deads if the total exceeds the population
        new_deads = int(config['MORTALITY_RATE'] * ls_infections[time_t - config['INFECTIVITY_TIME']]) if len(ls_infections) > config['INFECTIVITY_TIME'] else 0
        if new_deads >= config['TOTAL_POP']:
            new_deads = 0

    return new_infections, new_deads

def update_data(config, infection_rate, time_t, ls_infections, total_infections, total_deaths, data):
    """
    Update the simulation data by calculating new infections and deaths, and appending the results.
    
    Parameters:
        config (dict): Configuration dictionary containing global variables.
        infection_rate (float): The current infection rate at day time_t.
        time_t (int): The current day in the simulation.
        ls_infections (list): A list of the number of infections per day up to time_t.
        total_infections (int): The cumulative total number of infections up to time_t.
        total_deaths (int): The cumulative total number of deaths up to time_t.
        data (list): A list to store the simulation data for each day.
        
    Returns:
        tuple: A tuple containing the updated list of infections, total deaths, and data.
    """
    # Calculate new infections and deaths for the current day
    It, new_deads_t = calculate_new_infections_deads(config, infection_rate, time_t, ls_infections)
        
    # Update cumulative totals
    total_infections += It
    total_deaths += new_deads_t
    
    # Append the new data to the list
    ls_infections.append(It)
    data.append((time_t, It, total_infections, new_deads_t, total_deaths))
    
    return ls_infections, total_deaths, data

def simulate(config):
    """
    Simulate the spread of the infection over a specified number of days.
    
    Parameters:
        config (dict): Configuration dictionary containing global variables.
        
    Returns:
        pd.DataFrame: A DataFrame containing the simulation data with columns 
                      ['Time', 'Infected_per_day', 'Total_infections', 'Deads_per_day', 'Total_Deads'].
    """
    # Initialize response variables
    data, ls_infections = [], []
    total_infections, total_deaths = 0, 0
    
    # Initial infection rate
    infection_rate = np.log(config['INITIAL_R0']) / config['INFECTIVITY_TIME']
    
    # Simulate each day
    for t in range(config['TOTAL_DAYS']):
        # Update the infection rate based on the mask and vaccine conditions
        if config['DAY_FOR_VACCINE'] >= t >= config['DAY_FOR_MASKS']:
            infection_rate = update_infection_rate(config, config['INITIAL_R0'], config['FINAL_R0_MASK'], config['DELTA_R0'], config['DAY_FOR_MASKS'], t)
        elif t >= config['DAY_FOR_VACCINE']:
            infection_rate = update_infection_rate(config, config['FINAL_R0_MASK'], config['FINAL_R0_VACCINE'], config['DELTA_R0_VACCINE'], config['DAY_FOR_VACCINE'], t)
        
        # Update the simulation data for the current day
        ls_infections, total_deaths, data = update_data(config, infection_rate, t, ls_infections, total_infections, total_deaths, data)
    
    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data=data, columns=['Time', 'Infected_per_day', 'Total_infections', 'Deads_per_day', 'Total_Deads'])
    
    return df 


def plot_simmulation(config, df_simmulation):
    """
    Plot the results of the simulation, including the number of new infections per day,
    total infections, new deaths per day, and total deaths.

    Parameters:
        df_simmulation (pd.DataFrame): DataFrame containing the simulation results.

    Returns:
        None
    """
    # General figure configuration
    plt.figure(figsize=(15, 10))

    # Subplot 1: Number of new infections per day
    plt.subplot(221)
    plt.plot(df_simmulation['Time'], df_simmulation['Infected_per_day'], color='blue', label='New Infections')
    plt.title('Number of New Infected People Per Day')
    plt.xlabel('Days')
    plt.ylabel('Number of New Infected People')
    plt.grid(True)
    plt.legend()

    # Subplot 2: Total number of infections up to day t
    plt.subplot(222)
    plt.plot(df_simmulation['Time'], df_simmulation['Total_infections'], color='orange', label='Total Infections')
    plt.title('Total Number of Infected People Up to Day t')
    plt.xlabel('Days')
    plt.ylabel('Total Number of Infections')
    plt.grid(True)
    plt.legend()

    # Subplot 3: Number of new deaths per day
    plt.subplot(223)
    plt.plot(df_simmulation['Time'], df_simmulation['Deads_per_day'], color='red', label='New Deaths')
    plt.title('Number of New Deaths Per Day')
    plt.xlabel('Days')
    plt.ylabel('Number of New Deaths')
    plt.grid(True)
    plt.legend()

    # Subplot 4: Total number of deaths up to day t
    plt.subplot(224)
    plt.plot(df_simmulation['Time'], df_simmulation['Total_Deads'], color='purple', label='Total Deaths')
    plt.title('Total Number of Deaths Up to Day t')
    plt.xlabel('Days')
    plt.ylabel('Total Number of Deaths')
    plt.grid(True)
    plt.legend()

    # Adjust the spacing between subplots
    plt.tight_layout()

    # Save the figure
    plt.savefig(config['IMAGES_PATH']+'simulation_plots.png')

    # Show the figure
    plt.show()