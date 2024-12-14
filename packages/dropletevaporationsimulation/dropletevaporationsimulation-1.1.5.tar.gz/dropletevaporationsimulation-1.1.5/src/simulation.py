# src/simulation.py
"""This module defines the class DropletEvaporationModel and all its methods necessary for the computation.

    :return: _description_
    :rtype: DropletEvaporationModel
    """
from constants import *
from utils import interpolate_ode
from scipy.integrate import cumulative_trapezoid, solve_ivp
import numpy as np


class DropletEvaporationModel:
    def __init__(self):
        self.ug = 2 * np.exp(-10 * TIME_ARRAY)  # Axial velocity of gas phase

    def vapor_pressure(self, T, model_type="low"):
        """Calculate vapor pressure based on temperature and model type.

        :param T: Temperature
        :type T: Float
        :param model_type: Model type given Temperature (low or high), defaults to "low"
        :type model_type: str, optional
        :return: Vapor pressure
        :rtype: Float
        """
        if model_type == "low":
            return 10 ** (A1 - B1 / (T + C1))
        elif model_type == "high":
            return 10 ** (A2 - B2 / (T + C2))

    def calculate_mass_transfer_number(self, Pvap):
        """Compute the Spalding mass transfer number Bm.

        :param Pvap: Vapor pressure
        :type Pvap: Float
        :return: Spalding mass transfer number
        :rtype: Float
        """
        Yf_s = (Pvap * MF) / ((Pvap * MF) + (1 - Pvap) * MA)
        return Yf_s / (1 - Yf_s)

    def calculate_diameter_squared(self, ta, Bm, model="d2_law"):
        """Calculate D² over time using the chosen model.

        :param ta: Time array
        :type ta: array
        :param Bm: Spalding mass transfer number
        :type Bm: Float
        :param model: Choice of droplet evaporation model (d2 law or infinite liquid conductivity), defaults to "d2_law"
        :type model: str, optional
        :return: Droplet diameter squared
        :rtype: array
        """
        if model == "d2_law":
            Kv = ((LAMBDA / CP_A) / RHO_F) * np.log(1 + Bm)
            Dsquare = -4 * Kv * ta + DO**2
            return Dsquare
        elif model == "infinite_liquid_conductivity":
            Dsquare = (-4 * (RHO_A / RHO_F) * DV * SH * np.log(1 + Bm)) * ta + DO**2
            return Dsquare

    def calculate_droplet_temperature(self, ta, Bm, Dsquare):
        """Calculate the droplet temperature with values of the Infinite Liquid Conductivity model

        :param ta: Time array
        :type ta: array
        :param Bm: Spalding mass transfer number
        :type Bm: Float
        :param Dsquare: Droplet diameter squared
        :type Dsquare: array
        :return: Droplet temperature
        :rtype: OdeResult
        """
        f = (12 * LAMBDA) / (CP_F * RHO_F * Dsquare)
        g = (12 * LAMBDA * TA - 6 * H_FG * RHO_A * DV * SH * np.log(1 + Bm)) / (
            CP_F * RHO_F * Dsquare
        )
        tspan = [0, 5]  # defining time interval
        Tp0 = [TF]  # initial condition
        Tp = solve_ivp(interpolate_ode, tspan, Tp0, args=(ta, f, g))
        return Tp

    def calculate_droplet_velocity(self, ta, Dsquare):
        """Calculate droplet velocity over time using the chosen Dsquare.

        :param ta: Time array
        :type ta: array
        :param Dsquare: Droplet diameter squared
        :type Dsquare: array
        :return: Time and Velocity attributes of  Up
        :rtype: OdeResult
        """
        # Aerodynamics of droplet
        h1 = (18 * MU_A) / (Dsquare * RHO_F)
        k1 = (18 * MU_A) / (Dsquare * RHO_F) * self.ug
        tspan = [0, 4]  # defining time interval
        Up0 = [0]  # initial condition
        Up = solve_ivp(interpolate_ode, tspan, Up0, args=(ta, h1, k1))
        time = Up.t[:400]
        velocity = Up.y[0][:400]
        return time, velocity

    def calculate_droplet_position(self, time, velocity):
        """Calculate droplet velocity over time using the chosen Velocity.

        :param time: Time array of the velocity
        :type time: array
        :param velocity: Velocity attribute of the Up OdeResult
        :type velocity: 2D array
        :return: Droplet position
        :rtype: nupmy.ndarray
        """
        # Solving axial position Xp of droplet
        Xp = cumulative_trapezoid(velocity, time, initial=0)
        return Xp
