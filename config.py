# Simulation Inputs
TOTAL_DAYS = 365  # Number of days to simulate
TOTAL_POP = 3_000_000  # Total population size
N_INFECTED_POP = 4  # Initial number of infected people (I0)
INFECTIVITY_TIME = 2  # Infectivity period (Ti) in days
MORTALITY_RATE = 0.07  # Mortality rate (mu)

# Event Timing
DAY_FOR_MASKS = 14  # Day when mask-wearing is implemented
DAY_FOR_VACCINE = 170  # Day when vaccination starts

# Basic Reproduction Number (R0)
INITIAL_R0 = 3  # Initial R0 before any interventions
FINAL_R0_MASK = 1.1  # R0 after masks are fully implemented
FINAL_R0_VACCINE = 0.8  # R0 after vaccination is fully implemented

# Transition Periods
TRANSITION_DAYS_MASK = 20  # Number of days over which mask-wearing reduces R0
TRANSITION_DAYS_VACCINE = 250  # Number of days over which vaccination reduces R0

# Calculated Parameters
DELTA_R0 = (FINAL_R0_MASK - INITIAL_R0) / TRANSITION_DAYS_MASK  # Daily change in R0 due to masks
DELTA_R0_VACCINE = (FINAL_R0_VACCINE - FINAL_R0_MASK) / TRANSITION_DAYS_VACCINE  # Daily change in R0 due to vaccination