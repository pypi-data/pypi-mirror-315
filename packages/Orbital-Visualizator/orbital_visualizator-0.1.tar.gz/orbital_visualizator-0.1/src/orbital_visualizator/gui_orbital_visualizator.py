"""
    This module contains all functions to handle the graphic user interface including invoking
    a window, manage visibility within this GUI and handle submission of data entered by user in
    window's text widgets.
    Author : Baptiste LEBON
    Date : 16 december 2024
"""

from typing import Union
import tkinter as tk
from tkinter import messagebox, Text, Entry, Tk, Frame, Label
from skyfield.api import EarthSatellite
import numpy as np


def submit_parameters(
    option: str,
    entry_tle: Text,
    name_tle: Text,
    entry_param: list[Entry],
    window: Tk,
    orbital_parameters: list[Union[float, str]],
) -> None:
    """
    Handles the submission of orbital parameters from the user interface.

    This method is triggered when the submit button is clicked.
    This function is triggered when the submit button is clicked. It extracts
    and validates user inputs from the provided widgets, then updates the global
    Orbital_Parameters list.
    Used within the `select_data()` method.

    :param option: A string holding the user's choice between tle and keplerian
    :param entry_tle: A `tkinter.Text` widget containing the two lines element
    :param name_tle: A `tkinter.Text` widget containing the name of the satellite
    :param entry_param: A list of `tkinter.Entry` widgets for direct orbital parameters
    :param window: The `tkinter.Tk` instance of the user interface window.
    :param Orbital_Parameters: A global list to store the keplerian orbital parameters including
    TLE data or direct parameters.
    :return: None. The parameters are directly appended to the `Orbital_Parameters` list.
    """

    mu_earth = 398600.4418  # km^3 / s^2
    if option == "tle":
        tle_line_1 = entry_tle.get("1.0", "1.end").strip()
        tle_line_2 = entry_tle.get("2.0", "2.end").strip()
        if (tle_line_1) and (tle_line_2) and (name_tle):
            satellite = EarthSatellite(tle_line_1, tle_line_2, name_tle.get())
            orbital_parameters.append(
                (
                    mu_earth
                    / (
                        2
                        * np.pi
                        / (((2 * np.pi / (satellite.model.no_kozai * 60)) * 3600))
                    )
                    ** 2
                )
                ** (1 / 3)
            )
            orbital_parameters.append(satellite.model.ecco)
            orbital_parameters.append(satellite.model.inclo)  # in radian
            orbital_parameters.append(satellite.model.nodeo)  # in radian
            orbital_parameters.append(satellite.model.argpo)  # in radian
            orbital_parameters.append(satellite.model.mo)  # in radian
            orbital_parameters.append(satellite.name)
            window.quit()
            window.destroy()
        else:
            orbital_parameters.clear()
            messagebox.showwarning("Error", "Please enter a valid TLE and a name.")
    else:

        for i in range(6):
            if entry_param[i].get():
                orbital_parameters.append(float(entry_param[i].get()))
            else:
                break
        orbital_parameters.append(entry_param[6].get())

        if all(element for element in orbital_parameters):
            window.quit()
            window.destroy()
        else:
            orbital_parameters.clear()
            messagebox.showwarning(
                "Error", "Please enter valid numerical values for orbital parameters."
            )


def toggle_fields(
    option: str,
    label: Label,
    entry: Text,
    label_name: Label,
    name: Entry,
    parameters: Frame,
) -> None:
    """
    Manages visibility of fields in the GUI based on the choice made by the user: either
    TLE or direct orbital parameters.
    It is used within the `select_data()` method.

    :param option: A string containing the user's choice ("tle" or "keplerian").
    :param label: A `tkinter.Label` widget for the TLE input
    :param entry: A `tkinter.Text` widget where TLE data is entered.
    :param label_name: A `tkinter.Label` widget for the satellite's name (TLE option).
    :param name: A `Entry` tkinter.widget for entering the satellite's name (TLE option).
    :param parameters: A `tkinter.Frame` widget containing all input fields for direct orbital
     parameters.
    :return: None. The function directly modifies the visibility of the provided widgets.
    """
    print(option)
    if option == "tle":
        label.pack(pady=5)
        entry.pack(pady=5)
        label_name.pack(padx=5, pady=5)
        name.pack(padx=5, pady=5)
        parameters.pack_forget()
    else:
        label.pack_forget()
        entry.pack_forget()
        label_name.pack_forget()
        name.pack_forget()
        parameters.pack(pady=10)


def select_data(orbital_parameters: list, tles_option: str) -> None:
    """
    Configures and displays the GUI to enter TLE or direct orbital parameters.

    This method launches a GUI to allow the user to enter either TLE or direct orbital
    parameters (keplerian).
    The provided data are saved into the `Orbital_Parameters` list.
    :param Orbital_Parameters: A list containing the global orbital parameters
    :param tles_option: A string to choose format of input data, should be 'tle' or 'keplerian'
    :return: None. This function modifies the `Orbital_Parameters` list directly.
    """
    label = [
        "Major axis (a) [km] : ",
        "Eccentricity (e) :",
        "Inclination (i) [rad] :",
        "RAAN [rad] :",
        "Periapsis argument [rad] :",
        "True anomalie (M) [rad] :",
        "Name of the satellite: ",
    ]
    orbital_parameters_variable = ["a", "e", "i", "RAAN", "OMEGA", "M", "name"]
    entry_window = tk.Tk()  # main window creation
    entry_window.title("Orbital parameters selection")
    # icone = tk.PhotoImage(file="src\orbital_visualizator\orbito_logo.png")     #not working
    # entry_window.iconphoto(True, icone)

    # TLE
    frame_options = tk.Frame(entry_window)
    frame_options.pack(pady=10)  # Frame for TLE

    label_tle = tk.Label(entry_window, text="Please enter TLE (in two lines):")
    label_tle.pack(pady=5)  # Text box for TLE
    entry_tle = tk.Text(entry_window, width=70, height=2)
    entry_tle.pack(pady=5)
    entry_name_label = tk.Label(entry_window, text="Name of the satellite")
    entry_name_label.pack(padx=5, pady=5)
    entry_name_value = tk.Entry(entry_window)
    entry_name_value.pack(padx=5, pady=5)

    # Direct ortibal parameters
    frame_parameters = tk.Frame(entry_window)
    frame_parameters.pack(pady=10)  # Direct orbital parameters frame

    for i in range(7):
        label[i] = tk.Label(frame_parameters, text=label[i])
        label[i].grid(row=i, column=0, padx=5, pady=5)
        orbital_parameters_variable[i] = tk.Entry(frame_parameters)
        orbital_parameters_variable[i].grid(row=i, column=1, padx=5, pady=5)

    btn_submit = tk.Button(
        entry_window,
        text="Submit",
        command=lambda: submit_parameters(
            tles_option,
            entry_tle,
            entry_name_value,
            orbital_parameters_variable,
            entry_window,
            orbital_parameters,
        ),
    )
    btn_submit.pack(pady=20)  # Button for submission

    toggle_fields(
        tles_option,
        label_tle,
        entry_tle,
        entry_name_label,
        entry_name_value,
        frame_parameters,
    )  # Initialize visible fields

    entry_window.protocol("WM_DELETE_WINDOW", entry_window.quit)

    entry_window.mainloop()  # Keep the user interface opened
