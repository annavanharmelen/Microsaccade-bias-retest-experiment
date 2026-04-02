"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

from psychopy import visual
from numpy import zeros
from math import sqrt
from os import listdir, path

ECCENTRICITY = 6
DOT_SIZE = 0.1  # diameter of circle
OBJECT_SIZE = [4, 4]  # width, height
RESPONSE_DIAL_SIZE = 2  # radius of circle


def initialise_all_stimuli(stimuli_directory, settings):
    # Create fixation dot
    fixation_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](DOT_SIZE),
        pos=(0, 0),
        fillColor="#eaeaea",
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

    # Create dictionary of objects
    objects = {}
    for idx, file in enumerate(listdir(stimuli_directory)):
        image = visual.ImageStim(
            win=settings["window"],
            image=path.join(stimuli_directory, file),
            size=(
                settings["deg2pix"](OBJECT_SIZE[0]),
                settings["deg2pix"](OBJECT_SIZE[1]),
            ),
            units="pix",
        )
        objects.update({idx + 1: image})

    return {
        "fixation_dot": fixation_dot,
        "probe_circle": probe,
        "top_handle": top_handle,
        "bottom_handle": bottom_handle,
        "objects": objects,
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


def draw_one_object(item, orientation, colour, position, settings):
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

    return item


def draw_circle(item, pos=(0, 0), colour="#d4d4d4"):
    item.lineColor = colour
    item.pos = pos

    item.draw()


def create_stimuli_frame(stimuli_dict, object_ids, orientations, colours, settings):
    draw_fixation_dot(stimuli_dict["fixation_dot"])
    draw_one_object(
        stimuli_dict["objects"][object_ids[0]],
        orientations[0],
        colours[0],
        "left",
        settings,
    )
    draw_one_object(
        stimuli_dict["objects"][object_ids[1]],
        orientations[1],
        colours[1],
        "right",
        settings,
    )


def create_probe_cue_frame(stimuli, colour):
    draw_fixation_dot(stimuli["fixation_dot"], colour)
    draw_circle(stimuli["probe_circle"], colour="#eaeaea")
