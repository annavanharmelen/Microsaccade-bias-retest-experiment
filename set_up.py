"""
This file contains the functions necessary for
seting up the computer.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

from psychopy import visual
from psychopy.hardware.keyboard import Keyboard
from math import degrees, atan2, pi

GABOR_SIZE = 3  # diameter of Gabor


def get_monitor_and_dir(testing: bool):
    if testing:
        # laptop
        monitor = {
            "resolution": (2880, 1800),  # in pixels
            "Hz": 120,  # screen refresh rate in Hz
            "width": 30,  # in cm
            "distance": 50,  # in cm
        }

        directory = r"..\..\Data\test2"
        stimuli_directory = (
            r"..\..\Forms, explanation, documentation\m7 - test-retest\stimulus set"
        )

    else:
        # lab
        monitor = {
            "resolution": (1920, 1080),  # in pixels
            "Hz": 239,  # screen refresh rate in Hz
            "width": 53,  # in cm
            "distance": 70,  # in cm
        }

        directory = r"C:\Users\Anna_vidi\Desktop\microsaccade_data"

    return monitor, directory, stimuli_directory


def get_settings(monitor: dict, directory):
    # Initialise psychopy window
    window = visual.Window(
        color=([-0.5, -0.5, -0.5]),
        size=monitor["resolution"],
        units="pix",
        fullscr=True,
    )

    # Calculate number of visual degrees per pixel on the screen
    degrees_per_pixel = degrees(atan2(0.5 * monitor["width"], monitor["distance"])) / (
        0.5 * monitor["resolution"][0]
    )

    return dict(
        deg2pix=lambda deg: round(deg / degrees_per_pixel),
        dial_step_size=(0.5 * pi) / monitor["Hz"],
        window=window,
        keyboard=Keyboard(),
        mouse=visual.CustomMouse(win=window, visible=False),
        monitor=monitor,
        directory=directory,
    )
