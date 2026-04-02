"""
This file contains the functions necessary for
creating the interactive response dial at the end of a trial.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

from psychopy import event
from psychopy.hardware.keyboard import Keyboard
from math import cos, sin, degrees
from stimuli import draw_fixation_dot, draw_circle, RESPONSE_DIAL_SIZE
from time import time
from eyetracker import get_trigger


def turn_handle(pos, dial_step_size):
    x, y = pos
    pos = (
        x * cos(dial_step_size) + y * sin(dial_step_size),
        -x * sin(dial_step_size) + y * cos(dial_step_size),
    )

    # centre, distance, rad
    return pos


def get_report_orientation(key, turns, dial_step_size):
    report_orientation = degrees(turns * dial_step_size)

    if key == "z":
        report_orientation *= -1

    return report_orientation


def evaluate_response(report_orientation, target_orientation, key):
    report_orientation = round(report_orientation)

    difference = target_orientation - report_orientation

    if difference > 90:
        signed_difference = difference - 180
    elif difference < -90:
        signed_difference = difference + 180
    else:
        signed_difference = difference

    abs_difference = abs(signed_difference)
    performance = round(100 - abs_difference / 90 * 100)

    correct_key = (target_orientation > 0 and key == "m") or (
        target_orientation < 0 and key == "z"
    )

    return {
        "report_orientation": report_orientation,
        "performance": performance,
        "difference": difference,
        "signed_difference": signed_difference,
        "absolute_difference": abs_difference,
        "correct_key": correct_key,
    }


def draw_dial(stimuli, colour, settings):
    draw_circle(stimuli["probe_circle"], colour=colour)
    draw_circle(
        stimuli["top_handle"],
        pos=(settings["deg2pix"](0), settings["deg2pix"](RESPONSE_DIAL_SIZE)),
    )
    draw_circle(
        stimuli["bottom_handle"],
        pos=(settings["deg2pix"](0), settings["deg2pix"](-RESPONSE_DIAL_SIZE)),
    )


def get_response(
    stimuli,
    target_position,
    target_object,
    target_orientation,
    target_colour,
    settings,
    testing,
    eyetracker,
    additional_objects=[],
):
    keyboard: Keyboard = settings["keyboard"]
    window = settings["window"]

    # Check for pressed 'q'
    check_quit(keyboard)

    # These timing systems should start at the same time, this is almost true
    idle_reaction_time_start = time()
    keyboard.clock.reset()  # this reset ensures that premature key timings are relative to probe onset

    # Check if _any_ keys were prematurely pressed
    prematurely_pressed = [(p.name, p.rt) for p in keyboard.getKeys()]

    # Now clear keyboard before next response
    keyboard.clearEvents()

    turns = 0

    for item in additional_objects:
        item.draw()
        draw_circle(stimuli["probe_circle"], colour="#eaeaea")
        window.flip()

    # Wait indefinitely until the participant starts giving an answer
    keyboard.clearEvents()  # do it again to be sure
    pressed = event.waitKeys(keyList=["z", "m", "q"])

    response_started = time()

    if not testing and eyetracker:
        trigger = get_trigger(
            "response_onset",
            target_position,
            target_object,
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    if "m" in pressed:
        key = "m"
        rad = settings["dial_step_size"]
    elif "z" in pressed:
        key = "z"
        rad = -settings["dial_step_size"]
    if "q" in pressed:
        raise KeyboardInterrupt()

    draw_fixation_dot(stimuli["fixation_dot"], target_colour)
    draw_dial(stimuli, "#eaeaea", settings)

    # Stop rotating the moment either of the following happens:
    # - the participant released the rotation key
    # - a second passed
    while not keyboard.getKeys(keyList=[key]) and turns < settings["monitor"]["Hz"]:
        turns += 1

        stimuli["top_handle"].pos = turn_handle(stimuli["top_handle"].pos, rad)
        stimuli["bottom_handle"].pos = turn_handle(stimuli["bottom_handle"].pos, rad)

        for item in additional_objects:
            item.draw()

        if not additional_objects:
            draw_fixation_dot(stimuli["fixation_dot"], target_colour)

        stimuli["probe_circle"].draw()
        stimuli["top_handle"].draw()
        stimuli["bottom_handle"].draw()
        window.flip()

    # Compute both reaction times
    response_time = time() - response_started
    idle_reaction_time = response_started - idle_reaction_time_start

    if not testing and eyetracker:
        trigger = get_trigger("response_offset", target_position, target_object)
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Make sure keystrokes made during this trial don't influence the next
    keyboard.clearEvents()

    return {
        "idle_reaction_time_in_ms": round(idle_reaction_time * 1000, 2),
        "response_time_in_ms": round(response_time * 1000, 2),
        "key_pressed": key,
        "turns_made": turns,
        "premature_pressed": True if prematurely_pressed else False,
        "premature_key": (
            [k[0] for k in prematurely_pressed] if prematurely_pressed else None
        ),
        "premature_timing": (
            [round(k[1] * 1000, 2) for k in prematurely_pressed]
            if prematurely_pressed
            else None
        ),
        **evaluate_response(
            get_report_orientation(key, turns, settings["dial_step_size"]),
            target_orientation,
            key,
        ),
    }


def wait_for_key(key_list, keyboard):
    keyboard: Keyboard = keyboard
    keyboard.clearEvents()
    keys = event.waitKeys(keyList=key_list)

    return keys


def check_quit(keyboard):
    if keyboard.getKeys("q"):
        raise KeyboardInterrupt()
