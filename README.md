# Pandemic Simulation Project

This project simulates the spread of an infectious disease in a population over time. The goal is to model how the infection spreads through the population, the effect of interventions such as mask-wearing and vaccination, and the resulting number of infections and deaths. The project uses the SIR model (Susceptible, Infected, Recovered) to simulate infection rates and presents the results in a structured format.

## Theoretical Explanation

SIR model is the most commonly used mathematical model to describe how diseases are transmitted. It takes into account several factors that are described below:

### Infection Rate

For calculating the infection rate we use a simple exponential relationship that reflects how the disease spreads within a population. This rate is governed by the basic reproduction number $R_{0}$, which is the average number of secondary infections produced by an infected person in a fully susceptible population.

The infection rate $r$ is calculated as:

$$
r = \frac{\ln(R_{0})}{T_{i}}
$$

Where:
- $R_{0}$ is the basic reproduction number.
- $T_{i}$ is the infectious period (number of days an individual is contagious).
- $r$ is the rate at which the infection spreads through the population.

The infection rate changes throughout the simulation based on interventions like mask-wearing and vaccination, which lower $R_{0}$.

### Number of Infected Individuals $I(t)$

The number of new infections on a given day $t$ is given by a simple exponential relationship:

$$
I(t) = I_{0} \times e^{r \cdot t}
$$

Where:
- $I(t)$ is the number of people infected on day $t$.
- $I_{0}$ is the number of initially infected individuals.
- $r$ is the infection rate calculated above.
- $t$ is the current day of the simulation.

### New Deaths

Number of deaths on a given day t is related to the number of people who were infected T_{i} days earlier. This is relevant because there is a natural delay between the moment a person becomes infected and the moment they might die. This model assumes that the mortality rate μ (likelihood that a person who becomes infected will die from the illness) is constant and that all infected individuals have the same probability of dying after a constant time T_{i}​.

The number of new deaths each day is calculated as:

$$
\text{New\ Deaths}(t) = \mu \times I(t - T_{i})
$$

Where:
- $\mu$ is the mortality rate.
- $I(t - T_{i})$ is the number of people infected $T_{i}$ days earlier, where $T_{i}$ is the infectivity time (time from infection to death).

### Cumulative Number of Deaths $M(t)$

Analogously the cumulative number of deaths up to day $t$ is calculated by summing up the daily deaths:

$$
M(t) = \sum_{i=1}^{t} \mu \times I(i - T_{i})
$$

Where:
- $M(t)$ is the cumulative number of deaths up to day $t$.
- $I(i - T_{i})$ is the number of infections that occurred $T_{i}$ days earlier, and $\mu$ is the mortality rate.

### Interventions: Mask-Wearing and Vaccination

To simulate real-world scenarios, the model introduces interventions at specific points in time:
- **Mask-wearing** reduces the transmission rate $R_{0}$ by a certain factor after a specific day.
- **Vaccination** further reduces $R_{0}$ as more of the population becomes immune or less likely to spread the disease.

These interventions modify the infection rate as follows:

$$
R_{0}(t) =
\begin{cases}
R_{0} & \text{if } t < \text{mask day}, \\
R_{0_{\text{mask}}} & \text{if } \text{mask day} \leq t < \text{vaccine day}, \\
R_{0_{\text{vaccine}}} & \text{if } t \geq \text{vaccine day}
\end{cases}
$$

Where:
- $R_{0}$ is the initial reproduction number.
- $R_{0_{\text{mask}}}$ is the reproduction number after mask-wearing is implemented.
- $R_{0_{\text{vaccine}}}$ is the reproduction number after vaccination.

## Project Structure

The project is organized into several modules, each serving a specific purpose within the simulation framework.

### Modules

1. **`main.py`**
    - This is the entry point of the simulation. It loads the configuration variables (specified by the user), runs the simulation over a defined number of days, and saves the results of the simmulation as a csv file and images with plots.
    - It orchestrates the use of other modules (`utils.py`).

2. **`config.py`**
    - Contains all the global variables and configuration settings for the simulation, such as:
        - `TOTAL_DAYS`: Number of days to run the simulation.
        - `INITIAL_R0`, `FINAL_R0_MASK`, `FINAL_R0_VACCINE`: The reproduction numbers before and after interventions.
        - `INFECTIVITY_TIME`: The number of days an individual remains contagious.
        - `MORTALITY_RATE`: The percentage of infected people who die.
        - `DAY_FOR_MASKS` and `DAY_FOR_VACCINE`: Days when interventions (mask-wearing and vaccination) are introduced.
        - Paths to store data and images.

3. **`utils.py`**
    - Contains helper functions used in the simulation. These include:
        - **`update_infection_rate()`**: Updates the infection rate based on the current day and any interventions (mask or vaccine).
        - **`calculate_new_infections_deads()`**: Calculates new infections and deaths based on the infection rate and previous infections.
        - **`update_data()`**: Updates the simulation data (number of infected people, deaths, etc.) for each day.
        - **`simulate()`**: Runs the main simulation loop for the specified number of days, updating infection and death statistics over time.

4. **`testing.py`**
    - Contains unit tests for the different functions and modules in the project.

### How to Run the Project

To run the simulation, follow these steps:

1. **Clone the repository**:

```
git clone https://github.com/Mariog3497/Pandemic-Simul.git
```

This will download the entire project to your local system.

2. **Install Dependencies**:

The project requires certain Python packages to function. These are listed in the `requirements.txt` file. Install them by running the following command:

```
pip install -r requirements.txt
```

This will install all the necessary libraries, such as numpy, pandas, and matplotlib.

3. **Simmulation variables**:

4. **Run main file**:

### Example