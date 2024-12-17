"""
    This test allows to verify if the function plot_orbit doesn't crash.
    Author : Baptiste LEBON
    Date : 17 december 2024
"""

import matplotlib.pyplot as plt
from src.orbital_visualizator.plot_orbital_visualizator import plot_orbit


def test_display_orbit():
    """
    This function verifies that plot_orbit doesn't crash.
        :param: None.
        :return: None.
    """
    fig = plt.figure()
    space = fig.add_subplot(111, projection="3d")

    plot_orbit(
        space, orbital_parameters=[36000, 0.00025, 0.45, 0.48, 0.58, 1.25, "Test_Probe"]
    )
