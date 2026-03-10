"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

from psychopy import visual
from numpy import zeros
from math import sqrt

ECCENTRICITY = 6
DOT_SIZE = 0.1  # diameter of circle
BAR_SIZE = [0.6, 4]  # width, height
RESPONSE_DIAL_SIZE = 2  # radius of circle


def initialise_all_stimuli(settings):
    # Create fixation dot
    fixation_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](DOT_SIZE),
        pos=(0, 0),
        fillColor="#eaeaea",
    )

    # Create main stimulus
    bar_stimulus = visual.Rect(
        win=settings["window"],
        units="pix",
        width=settings["deg2pix"](BAR_SIZE[0]),
        height=settings["deg2pix"](BAR_SIZE[1]),
        pos=(0, 0),
    )

    # Create main probe
    probe = visual.Circle(
        win=settings["window"],
        radius=settings["deg2pix"](RESPONSE_DIAL_SIZE),
        lineWidth=settings["deg2pix"](0.1),
        fillColor=None,
    )

    # Create probe handles
    top_handle = visual.Circle(
        win=settings["window"],
        radius=settings["deg2pix"](RESPONSE_DIAL_SIZE / 15),
        lineWidth=settings["deg2pix"](0.1),
        pos=(0, 0),
        lineColor="#eaeaea",
        fillColor=settings["window"].color,
    )

    bottom_handle = visual.Circle(
        win=settings["window"],
        radius=settings["deg2pix"](RESPONSE_DIAL_SIZE / 15),
        lineWidth=settings["deg2pix"](0.1),
        pos=(0, 0),
        lineColor="#eaeaea",
        fillColor=settings["window"].color,
    )

    return {
        "fixation_dot": fixation_dot,
        "bar": bar_stimulus,
        "probe_circle": probe,
        "top_handle": top_handle,
        "bottom_handle": bottom_handle,
    }


def show_text(input, window, pos=(0, 0), colour="#ffffff"):
    textstim = visual.TextStim(
        win=window, font="Aptos", text=input, color=colour, pos=pos, height=22
    )

    textstim.draw()


def draw_fixation_dot(dot_item, colour="#eaeaea"):
    # Set colour
    dot_item.fillColor = colour

    # Draw both components
    dot_item.draw()


def draw_one_bar(item, orientation, colour, position, settings):
    # Check input
    if position == "left":
        pos = (-settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "right":
        pos = (settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "middle":
        pos = (0, 0)
    else:
        raise Exception(f"Expected 'left' or 'right', but received {position!r}. :(")

    # Draw stimulus
    item.pos = pos
    item.ori = orientation
    item.setColor(colour)
    item.draw()


def draw_circle(item, pos=(0, 0), colour="#d4d4d4"):
    item.lineColor = colour
    item.pos = pos

    item.draw()


def create_stimuli_frame(
    stimuli, orientations, colours, settings
):
    draw_fixation_dot(stimuli["fixation_dot"])
    draw_one_bar(stimuli["bar"], orientations[0], colours[0], "left", settings)
    draw_one_bar(stimuli["bar"], orientations[1], colours[1], "right", settings)


def create_probe_cue_frame(stimuli, colour):
    draw_fixation_dot(stimuli["fixation_dot"], colour)
    draw_circle(stimuli["probe_circle"], colour="#eaeaea")
