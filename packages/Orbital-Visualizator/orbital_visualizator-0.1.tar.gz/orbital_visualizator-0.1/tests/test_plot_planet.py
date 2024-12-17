"""
    This test allows to verify if the function plot_central_body doesn't crash.
    Author : Baptiste LEBON
    Date : 17 december 2024
"""

import matplotlib.pyplot as plt
from src.orbital_visualizator.plot_orbital_visualizator import plot_central_body


def test_display_planete():
    """
    This function verifies that plot_central doesn't crash.
        :param: None.
        :return: None.
    """
    fig = plt.figure()
    space = fig.add_subplot(111, projection="3d")

    plot_central_body(space, 6370, "b")
