"""
Main script for the Droplet Evaporation Simulation project.

This script initializes the simulation parameters, computes the evaporation
models, and generates plots for droplet properties over time.
"""

import constants
from simulation import DropletEvaporationModel
from plots import (
    plot_velocity,
    plot_diameter_squared,
    plot_droplet_temperature,
    plot_droplet_velocity,
    plot_droplet_position,
)


def main():
    """Main function, runs the simulation and plots the results."""

    print("\nSimulation started!\n")

    # Update the constants or keep the default values (n-Decane and air)
    constants.update_constants()

    # Initialize the evaporation model
    model = DropletEvaporationModel()

    # Compute gas-phase velocity over time
    ug = model.ug
    plot_velocity(constants.TIME_ARRAY, ug)

    # Calculate vapor pressure for low and high temperature ranges
    Pvap1 = model.vapor_pressure(constants.TF, model_type="low")
    Pvap2 = model.vapor_pressure(constants.TF, model_type="high")

    # Compute Spalding mass transfer numbers
    Bm1 = model.calculate_mass_transfer_number(Pvap1)
    Bm2 = model.calculate_mass_transfer_number(Pvap2)

    # Compute D² evolution using D² law and infinite liquid conductivity models
    diameter_squared_d2_law = model.calculate_diameter_squared(
        constants.TIME_ARRAY, Bm1, model="d2_law"
    )
    diameter_squared_inf_conductivity = model.calculate_diameter_squared(
        constants.TIME_ARRAY, Bm2, model="infinite_liquid_conductivity"
    )

    # Normalize results for plotting
    normalized_d2_law = diameter_squared_d2_law / constants.DO**2
    normalized_inf_conductivity = diameter_squared_inf_conductivity / constants.DO**2

    # Plot the D² evolution for both models
    plot_diameter_squared(
        constants.TIME_ARRAY, normalized_d2_law, "D² Evolution (D² Law)"
    )
    plot_diameter_squared(
        constants.TIME_ARRAY,
        normalized_inf_conductivity,
        "D² Evolution (Infinite Liquid Conductivity)",
    )

    # Compute and plot droplet temperature evolution
    droplet_temperature = model.calculate_droplet_temperature(
        constants.TIME_ARRAY, Bm2, diameter_squared_inf_conductivity
    )
    plot_droplet_temperature(droplet_temperature)

    # Compute droplet axial velocity evolution for both models
    time_d2_law, droplet_velocity_d2_law = model.calculate_droplet_velocity(
        constants.TIME_ARRAY, diameter_squared_d2_law
    )
    time_inf_conductivity, droplet_velocity_inf_conductivity = (
        model.calculate_droplet_velocity(
            constants.TIME_ARRAY, diameter_squared_inf_conductivity
        )
    )

    # Plot the axial velocity evolution for both models
    plot_droplet_velocity(time_d2_law, droplet_velocity_d2_law, "D² Law")
    plot_droplet_velocity(
        time_inf_conductivity,
        droplet_velocity_inf_conductivity,
        "Infinite Liquid Conductivity Model",
    )

    # Compute and plot droplet axial position evolution (D² Law)
    droplet_position_d2_law = model.calculate_droplet_position(
        time_d2_law, droplet_velocity_d2_law
    )
    plot_droplet_position(time_d2_law, droplet_position_d2_law, "D² Law")

    # Compute and plot droplet axial position evolution (Infinite Liquid Conductivity Model)
    droplet_position_inf_conductivity = model.calculate_droplet_position(
        time_inf_conductivity, droplet_velocity_inf_conductivity
    )
    plot_droplet_position(
        time_inf_conductivity,
        droplet_position_inf_conductivity,
        "Infinite Liquid Conductivity Model",
    )

    # Minimum length of combustor before droplet evaporation
    Min_length_d2_law = droplet_position_d2_law[-1]
    Min_length_inf_conductivity = droplet_position_inf_conductivity[-1]

    print(
        "\nMinimum length for complete evaporation (D^2 Law): ",
        round(Min_length_d2_law, 6),
        " m.",
    )
    print(
        "Minimum length for complete evaporation (Infinite liquid conductivity model): ",
        round(Min_length_inf_conductivity, 6),
        " m.",
    )

    # End of simulation
    print("\nSimulation complete. Plots generated.")


if __name__ == "__main__":
    main()
