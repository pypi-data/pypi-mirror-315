import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_statistics(simulations, initial_value):
    """
    Calculate statistical summaries for the given simulation results.
    :param simulations: Simulation results (2D array: paths x time steps)
    :param initial_value: The initial value of the simulation (scalar)
    :return: Pandas DataFrame containing statistics and exceedance counts
    """
    # Probability levels (proportion of simulations above the initial value)
    p_level = np.mean(simulations > initial_value, axis=0)

    # Quantiles
    probability_levels = [99, 90, 10, 1]
    quantiles = {
        f"Quantile {p}%": np.percentile(simulations, p, axis=0) for p in probability_levels
    }

    # Mean across paths for each time step
    mean_values = np.mean(simulations, axis=0)

    # Calculate Exceedance: Check if initial value exceeds 99% or falls below 1%
    upper_exceedance = (initial_value > quantiles["Quantile 99%"]).sum()
    lower_exceedance = (initial_value < quantiles["Quantile 1%"]).sum()

    # Combine into a DataFrame
    stats_df = pd.DataFrame({
        "P_LEVEL": p_level,
        "Mean": mean_values,
        **quantiles
    })

    # Add exceedance stats as metadata to the DataFrame
    stats_df.attrs["Upper Exceedance"] = upper_exceedance
    stats_df.attrs["Lower Exceedance"] = lower_exceedance

    return stats_df

def display_statistics(stats_df, time):
    """
    Display the calculated statistics and exceedance counts.
    :param stats_df: DataFrame containing statistics
    :param time: Time array corresponding to the simulation
    """
    stats_df.insert(0, "Time", time)  # Add time as the first column
    
    # Print exceedance information
    upper_exceedance = stats_df.attrs["Upper Exceedance"]
    lower_exceedance = stats_df.attrs["Lower Exceedance"]

    print("\nExceedance Statistics:")
    print(f"  Upper Exceedance (Initial > Quantile 99%): {upper_exceedance}")
    print(f"  Lower Exceedance (Initial < Quantile 1%): {lower_exceedance}")
    
    # Print the statistical summary
    print("\nStatistical Summary:")
    print(stats_df)
    return stats_df

def plot_simulation(time, simulations, num_paths=None, title="Simulation Paths", xlabel="Time (Years)", ylabel="Value"):
    """
    Plot a subset of simulation paths using Matplotlib.
    :param time: Time array
    :param simulations: Simulation results (2D array: paths x time steps)
    :param num_paths: Number of paths to plot (if None, user will be prompted)
    :param title: Title of the plot
    :param xlabel: Label for the x-axis
    :param ylabel: Label for the y-axis
    """
    if num_paths is None:
        try:
            num_paths = int(input(f"Enter the number of paths to plot (max {simulations.shape[0]}): "))
            if num_paths <= 0 or num_paths > simulations.shape[0]:
                raise ValueError("Invalid number of paths!")
        except ValueError as e:
            print(f"Error: {e}. Using default value of 10 paths.")
            num_paths = 10  # Default value

    plt.figure(figsize=(12, 6))
    for i in range(min(num_paths, simulations.shape[0])):  # Plot up to num_paths
        plt.plot(time, simulations[i, :], lw=1, alpha=0.7)

    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()
