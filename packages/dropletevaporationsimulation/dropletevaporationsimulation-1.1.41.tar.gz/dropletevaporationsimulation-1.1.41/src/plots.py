# src/plots.py
"""This module defines the functions for plotting of the evolution of physical quantities 
    """
import matplotlib.pyplot as plt


def plot_velocity(time, ug):
    """Plots the evolution of the volecity of the Gas phase over time

    :param time: time array
    :type time: array
    :param ug: Velocity function of the gas phase
    :type ug: array
    """
    plt.figure()
    plt.plot(time, ug)
    plt.title("Axial velocity of gas phase")
    plt.xlabel("time (s)")
    plt.ylabel("Ug(t) (m/s)")
    plt.show()


def plot_diameter_squared(time, diameter_squared, title):
    """Plots the evolution of the squared diameter of the droplet over time

    :param time: time array
    :type time: array
    :param diameter_squared: Droplet diameter squared
    :type diameter_squared: array
    :param title: Title of the plot (depends on the chosen model)
    :type title: str
    """
    plt.figure()
    plt.plot(time, diameter_squared)
    plt.axis([0, 4, 0, 1])
    plt.xlabel("time (s)")
    plt.ylabel("(D/Do)^2")
    plt.title(title)
    plt.show()


def plot_droplet_temperature(droplet_temperature):
    """Plots the evolution of the droplet temperature over time

    :param droplet_temperature: Droplet temperature
    :type droplet_temperature: OdeResult
    """
    plt.figure()
    plt.plot(droplet_temperature.t, droplet_temperature.y[0])
    plt.xlabel("time (s)")
    plt.ylabel("Tp (K)")
    plt.title(
        "Evolution of droplet temperature over time (Infinite liquid conductivity model)"
    )
    plt.axis([0, 0.5, 300, 450])
    plt.show()


def plot_droplet_velocity(time, velocity, title):
    """Plots the evolution of the droplet axial velocity over time

    :param time: time array attribute of the computed OdeResult
    :type time: array
    :param velocity: velocity array attribute of the computed OdeResult
    :type velocity: 2D array
    :param title: Title of the plot (depends on the chosen model)
    :type title: str
    """
    plt.figure()
    plt.plot(time, velocity)
    plt.xlabel("time (s)")
    plt.ylabel("Up (m/s)")
    plt.title("Evolution of droplet axial velocity over time - " + title)
    plt.show()


def plot_droplet_position(time, position, title):
    """Plots the evolution of the position of the droplet over time

    :param time: time array of the velocity
    :type time: array
    :param position: Axial position of the droplet
    :type position: numpy.ndarray
    :param title: Title of the plot (depends on the chosen model)
    :type title: str
    """
    plt.figure()
    plt.plot(time, position)
    plt.xlabel("time (s)")
    plt.ylabel("Xp (m)")
    plt.title("Evolution of droplet axial position over time - " + title)
    plt.show()
