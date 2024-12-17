"""
    This test allows to verify the function orbit_calculation converts well Keplerian coordinates
    into Cartesian coordinates.
    Author : Baptiste LEBON
    Date : 17 december 2024
"""
import pytest
from src.orbital_visualizator.keplerian_to_cartesian_convertor import orbit_calculation



def test_calcul_orbit():
    """
    This function test convertion from Keplerian to Cartesian coordinates for a satellite with
    the following orbit:
        a = 36000 km
        e = 0.00025
        i = 0.45 rad
        RAAN = 0.48 rad
        OMEGA = 0.58 rad
        M = 1.25 rad
    These values were taken randomly just to check.

    :param: None.
    :return: None.
    """

    x, y, z = orbit_calculation(
        orbital_parameters=[36000, 0.00025, 0.45, 0.48, 0.58, 1.25, "Test_Probe"],
        theta=1.25,
    )

    assert x == pytest.approx(
        -22312.2, rel=0.1
    )   #Orbit_Calculation contains trigonometric function hence approximation for assert tests
    assert y == pytest.approx(23642.43, rel=0.1)
    assert z == pytest.approx(15459.52, rel=0.1)
