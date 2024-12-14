# src/constants.py
"""This module initialize the constants. For a different fuel, the values can be changed under #Droplet properties.
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
