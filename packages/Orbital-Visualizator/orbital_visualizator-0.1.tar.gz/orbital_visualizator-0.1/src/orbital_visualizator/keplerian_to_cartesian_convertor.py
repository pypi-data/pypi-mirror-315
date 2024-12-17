"""
    This module is used to convert Keplerian parameters into Cartesian parameters in the J2000
    frame.
    Author : Baptiste LEBON
    Date : 16 december 2024
"""

from typing import Union, Tuple
import numpy as np


def orbit_calculation(
    orbital_parameters: list, theta: Union[float, np.ndarray]
) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Converts Keplerian parameters into Cartesian coordinates in the inertial frame J2000.
    :param orbital_parameters: List of Keplerian parameters provided by the user.
    :param theta: The true anomaly of the satellite. This can be a float (for a specific
    position)or an np.ndarray (for orbit propagation over time).
    :return: Cartesian coordinates (x, y, z) of the orbit in the inertial frame J2000.
    The output type matches the input `theta` (float or np.ndarray).
    """
    r = (
        orbital_parameters[0]
        * (1 - orbital_parameters[1] ** 2)
        / (1 + orbital_parameters[1] * np.cos(theta))
    )
    x = r * (
        np.cos(orbital_parameters[4]) * np.cos(theta + orbital_parameters[3])
        - np.sin(orbital_parameters[4])
        * np.sin(theta + orbital_parameters[3])
        * np.cos(orbital_parameters[2])
    )
    y = r * (
        np.sin(orbital_parameters[4]) * np.cos(theta + orbital_parameters[3])
        + np.cos(orbital_parameters[4])
        * np.sin(theta + orbital_parameters[3])
        * np.cos(orbital_parameters[2])
    )
    z = r * (np.sin(theta + orbital_parameters[3]) * np.sin(orbital_parameters[2]))
    return x, y, z
