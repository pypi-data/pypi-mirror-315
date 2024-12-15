# src/constants.py
"""This module initialize the constants. 
For a different fuel, the values can be changed under #Droplet properties.
    """
import numpy as np

# Time array for simulation
TIME_ARRAY = np.linspace(0, 4, 1000)

# Droplet properties
DO = 50e-6  # Initial diameter (m)
RHO_F = 730  # Density (kg/m^3)
CP_F = 2440  # Specific heat (J/kg/K)
H_FG = 350000  # Latent heat of evaporation (J/kg)
DV = 6.5e-6  # Mass diffusivity of vapor in air (m^2/s)
MF = 0.142  # Molecular weight (kg/mol)
TF = 300  # Initial temperature (K)

# Vapor pressure constants
A1, B1, C1 = 0.21021, 440.616, -156.896
A2, B2, C2 = 4.07857, 1501.268, -78.67

# Gas-phase properties
LAMBDA = 0.02662  # Thermal conductivity (W/m/K)
RHO_A = 1.12  # Density (kg/m^3)
MU_A = 18e-6  # Dynamic viscosity (Ns/m^2)
MA = 0.029  # Molecular weight (kg/mol)
TA = 400  # Far-field temperature (K)
CP_A = 1014  # Specific heat (J/kg/K)

# Sherwood number
SH = 2


def update_constants():
    """CLI to update constants in src.constants or use the default values."""
    print("Welcome to the Constants Updater CLI!\n")
    use_default = (
        input("Would you like to use the default values? (yes/no): ").strip().lower()
    )

    if use_default in ["yes", "y"]:
        print("Using default values.")
        return

    print(
        "\nEnter new values for the constants. Press Enter to skip and keep the default value.\n"
    )

    def get_user_input(prompt, default, cast_type):
        """Helper function to get user input with a default value."""
        user_input = input(f"{prompt} (default: {default}): ").strip()
        return cast_type(user_input) if user_input else default

    # Update Droplet properties
    print("\nUpdate Droplet properties\n")
    global DO, RHO_F, CP_F, H_FG, DV, MF, TF
    DO = get_user_input("Initial diameter DO (m)", DO, float)
    RHO_F = get_user_input("Density RHO_F (kg/m^3)", RHO_F, float)
    CP_F = get_user_input("Specific heat CP_F (J/kg/K)", CP_F, float)
    H_FG = get_user_input("Latent heat of evaporation H_FG (J/kg)", H_FG, float)
    DV = get_user_input("Mass diffusivity of vapor DV (m^2/s)", DV, float)
    MF = get_user_input("Molecular weight MF (kg/mol)", MF, float)
    TF = get_user_input("Initial temperature TF (K)", TF, float)

    # Update Vapor pressure constants
    print("\nUpdate Vapor pressure constants\n")
    global A1, B1, C1, A2, B2, C2
    A1 = get_user_input("Vapor pressure constant A1", A1, float)
    B1 = get_user_input("Vapor pressure constant B1", B1, float)
    C1 = get_user_input("Vapor pressure constant C1", C1, float)
    A2 = get_user_input("Vapor pressure constant A2", A2, float)
    B2 = get_user_input("Vapor pressure constant B2", B2, float)
    C2 = get_user_input("Vapor pressure constant C2", C2, float)

    # Update Gas-phase properties
    print("\nUpdate Gas-phase properties\n")
    global LAMBDA, RHO_A, MU_A, MA, TA, CP_A
    LAMBDA = get_user_input("Thermal conductivity LAMBDA (W/m/K)", LAMBDA, float)
    RHO_A = get_user_input("Density RHO_A (kg/m^3)", RHO_A, float)
    MU_A = get_user_input("Dynamic viscosity MU_A (Ns/m^2)", MU_A, float)
    MA = get_user_input("Molecular weight MA (kg/mol)", MA, float)
    TA = get_user_input("Far-field temperature TA (K)", TA, float)
    CP_A = get_user_input("Specific heat CP_A (J/kg/K)", CP_A, float)

    # Update Sherwood number
    global SH
    SH = get_user_input("Sherwood number SH", SH, float)

    print("\nConstants updated successfully!\n")
