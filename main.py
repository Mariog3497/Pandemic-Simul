from utils import *
import config

if __name__ == "__main__":

    # Load configuration variables
    config_vars = vars(config)

    # Execute simmulation
    df_results = simulate(config_vars)
        
    # Save simmulation results in a csv file
    df_results.to_csv(config_vars['DATA_PATH']+"simulation_results.csv", index=False)

    # Create simmulation plots and save them
    plot_simmulation(config_vars, df_results)