"""
    These test allow to verify if the function submit_parameters well interpreted
    datas from user to good format data
    into Cartesian coordinates.
    Author : Baptiste LEBON
    Date : 17 december 2024
"""

from tkinter import Text, Tk, Entry
import pytest
from src.orbital_visualizator.gui_orbital_visualizator import submit_parameters


def test_submit():
    """
    This function verifies if the function submit_parameters well interpret
    datas from user to good format data
    Data entered by user are the following:

                        For TLE  (ISS)

        1 25544U 98067A   14273.50403866  .00012237  00000-0  21631-3 0  1790
        2 25544  51.6467 297.5710 0002045 126.1182  27.2142 15.50748592907666

                        For keplerian
        a=36000 km
        e=0.002
        i= 0.25 rad
        raan= 0.35 rad
        omega= 0.56 rad
        m= 1.87 rad

        :param: None.
        :return: None.
    """
    data_match = [
        [
            6792.68,
            0.2,
            0.0002045,
            0.000001,
            0.901405,
            0.02,
            5.193594,
            0.02,
            2.201178,
            0.02,
            0.474977,
            0.02,
            "ISS",
        ],
        [36000, 0, 0.002, 0, 0.25, 0, 0.35, 0, 0.56, 0, 1.87, 0, "Test_Satellite"],
    ]
    option = ["tle", "keplerian"]

    for j in range(2):

        window = Tk()
        dummy_text = Text(window)
        dummy_text.insert(
            1.0,
            "1 25544U 98067A   14273.50403866  .00012237  00000-0  21631-3 0  1790\n",
        )
        dummy_text.insert(
            2.0, "2 25544  51.6467 297.5710 0002045 126.1182  27.2142 15.50748592907666"
        )
        dummy_tle = Entry(window)
        dummy_tle.insert(0, "ISS")
        a = Entry(window)
        a.insert(0, 36000)
        e = Entry(window)
        e.insert(0, 0.002)
        i = Entry(window)
        i.insert(0, 0.25)
        raan = Entry(window)
        raan.insert(0, 0.35)
        omega = Entry(window)
        omega.insert(0, 0.56)
        m = Entry(window)
        m.insert(0, 1.87)
        dummy_name = Entry(window)
        dummy_name.insert(0, "Test_Satellite")
        dummy_entries = [a, e, i, raan, omega, m, dummy_name]
        orbital_parameters = []

        submit_parameters(
            option[j], dummy_text, dummy_tle, dummy_entries, window, orbital_parameters
        )

        assert orbital_parameters[0] == pytest.approx(
            data_match[j][0], rel=data_match[j][1]
        )
        assert orbital_parameters[1] == pytest.approx(
            data_match[j][2], rel=data_match[j][3]
        )
        assert orbital_parameters[2] == pytest.approx(
            data_match[j][4], rel=data_match[j][5]
        )
        assert orbital_parameters[3] == pytest.approx(
            data_match[j][6], rel=data_match[j][7]
        )
        assert orbital_parameters[4] == pytest.approx(
            data_match[j][8], rel=data_match[j][9]
        )
        assert orbital_parameters[5] == pytest.approx(
            data_match[j][10], rel=data_match[j][11]
        )
        assert orbital_parameters[6] == data_match[j][12]

        if option[j] == "tle":
            print("TLE asserts PASSED!")
        else:
            print("Keplerian asserts PASSED!")
