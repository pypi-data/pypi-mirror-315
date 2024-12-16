# src/simulation.py
"""This module defines the class DropletEvaporationModel and all its methods.
    """
from scipy.integrate import cumulative_trapezoid, solve_ivp
import numpy as np

from . import constants
from .utils import interpolate_ode


class DropletEvaporationModel:
    """This class contains all the methods to compute the droplet's evaporation and dynamics."""

    def __init__(self):
        self.ug = 2 * np.exp(-10 * constants.TIME_ARRAY)  # Axial velocity of gas phase

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
            return 10 ** (constants.A1 - constants.B1 / (T + constants.C1))
        elif model_type == "high":
            return 10 ** (constants.A2 - constants.B2 / (T + constants.C2))

    def calculate_mass_transfer_number(self, Pvap):
        """Compute the Spalding mass transfer number Bm.

        :param Pvap: Vapor pressure
        :type Pvap: Float
        :return: Spalding mass transfer number
        :rtype: Float
        """
        Yf_s = (Pvap * constants.MF) / (
            (Pvap * constants.MF) + (1 - Pvap) * constants.MA
        )
        return Yf_s / (1 - Yf_s)

    def calculate_diameter_squared(self, ta, Bm, model="d2_law"):
        """Calculate D² over time using the chosen model.

        :param ta: Time array
        :type ta: array
        :param Bm: Spalding mass transfer number
        :type Bm: Float
        :param model: Choice of droplet evaporation model, defaults to "d2_law"
        :type model: str, optional
        :return: Droplet diameter squared
        :rtype: array
        """
        if model == "d2_law":
            Kv = ((constants.LAMBDA / constants.CP_A) / constants.RHO_F) * np.log(
                1 + Bm
            )
            Dsquare = -4 * Kv * ta + constants.DO**2
            return Dsquare
        elif model == "infinite_liquid_conductivity":
            Dsquare = (
                -4
                * (constants.RHO_A / constants.RHO_F)
                * constants.DV
                * constants.SH
                * np.log(1 + Bm)
            ) * ta + constants.DO**2
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
        f = (12 * constants.LAMBDA) / (constants.CP_F * constants.RHO_F * Dsquare)
        g = (
            12 * constants.LAMBDA * constants.TA
            - 6
            * constants.H_FG
            * constants.RHO_A
            * constants.DV
            * constants.SH
            * np.log(1 + Bm)
        ) / (constants.CP_F * constants.RHO_F * Dsquare)
        tspan = [0, 5]  # defining time interval
        Tp0 = [constants.TF]  # initial condition
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
        h1 = (18 * constants.MU_A) / (Dsquare * constants.RHO_F)
        k1 = (18 * constants.MU_A) / (Dsquare * constants.RHO_F) * self.ug
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
