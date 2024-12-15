# src/utils.py
"""This modules defines utils functions.   

    """
import numpy as np


def interpolate_ode(t, y, ta, f, g):
    """Interpolates time dependant functions over a new time array

    :param t: _description_
    :type t: array
    :param y: default ODE solution
    :type y: array
    :param ta: _description_
    :type ta: array
    :param f: time dependant function 1
    :type f: array
    :param g: time dependant function 2
    :type g: array
    :return: Returns the time derivative of the function
    :rtype: array
    """
    f_interp = np.interp(t, ta, f)
    g_interp = np.interp(t, ta, g)
    return -f_interp * y + g_interp
