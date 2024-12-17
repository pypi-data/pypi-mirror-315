"""
    This module allows to plot central bodies, satellites' orbits and position in a 3D 
    representation.
    Author : Baptiste LEBON
    Date : 16 december 2024
"""

from typing import Union
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from .keplerian_to_cartesian_convertor import orbit_calculation


def plot_central_body(space: Axes3D, radius: Union[int, float], color: str) -> None:
    """
    Plots the surface of the central body around which the satellite orbits.

    :param space: The 3D matplotlib axes (Axes3D) where the central body will be plotted.
    :param radius: the radius of the central body in km (e.g. 6371 km for Earth).
    :param color: the color of the sphere representing the central body.
    :return: None.
    """
    u = np.linspace(
        0, 2 * np.pi, 100
    )  # 100 points array containing phi angles (in spheric coordinate system)
    v = np.linspace(
        0, np.pi, 100
    )  # 100 points array containing theta angles (in spheric coordinate system)
    x = radius * np.outer(
        np.cos(u), np.sin(v)
    )  # creation of matrix of points for a sphere (using outer products of arrays)
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    space.plot_surface(x, y, z, color=color, alpha=0.5)  # plot of the sphere in space


def plot_orbit(space: Axes3D, orbital_parameters: list) -> None:
    """
    Displays the orbit based on the Keplerian orbital parameters provided by the user in
    the specified domain.
    It also display the satellite's position based on its mean anomaly angle.

    :param space: The 3D matplotlib axes (Axes3D) where the central body will be plotted.
    :param orbital_parameters: A list containing all Keplerian orbital parameters entered by the
    user in the following format ['Major axis (a)[km]','Eccentricity (e)','Inclination (i) [rad]',
    'RAAN [rad]','Periapsis argument [rad]','True anomalie (M) [rad]','Name of the satellite'].
    :return: None. The orbit and satellite position are displayed directly on the provided Axes3D
    object.
    """
    theta = np.linspace(0, 2 * np.pi, 100)
    x, y, z = orbit_calculation(orbital_parameters, theta)
    space.plot(x, y, z, color="r")
    x, y, z = orbit_calculation(orbital_parameters, orbital_parameters[5])
    space.scatter(
        x, y, z, color="black", s=50, label="Satellite"
    )  # Black dot representing the satellite
