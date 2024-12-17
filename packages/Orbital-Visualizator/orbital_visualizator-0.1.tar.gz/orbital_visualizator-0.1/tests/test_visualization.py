"""
    This test allows to verify if the function orbite_vizalization works properly without any bug.
    Author : Baptiste LEBON
    Date : 17 december 2024
"""

from src.orbital_visualizator.orbital_visualizator_app import orbit_visualizator


def test_application():
    """
    This function verifies if the function orbite_vizalization works properly without any bug.
    Data entered by user are the following:
        datasource: "tle"

    :param: None.
    :return: None.
    """
    datasource = "tle"

    orbit_visualizator(datasource)
