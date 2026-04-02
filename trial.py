"""
This file contains the functions necessary for
creating and running a single trial start-to-finish,
including eyetracker triggers.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

from psychopy import visual
from psychopy.core import wait
from time import time, sleep
from response import get_response, check_quit
from stimuli import (
    draw_fixation_dot,
    create_stimuli_frame,
    show_text,
    create_probe_cue_frame,
)
from eyetracker import get_trigger
import random

# COLOURS = blue, pink, green, orange
COLOURS = [
    [(rgb_value / 128 - 1) for rgb_value in rgb_triplet]
    for rgb_triplet in [[19, 146, 206], [217, 103, 241], [101, 148, 14], [238, 104, 60]]
]


def generate_trial_characteristics(target_object, target_position):
    # Decide on random colours of stimulus + target
    [target_colour, distractor_colour] = random.sample(COLOURS, 2)

    # Create random stimuli orientations
    [target_orientation, distractor_orientation] = [
        random.choice([-1, 1]) * random.randint(5, 85),
        random.choice([-1, 1]) * random.randint(5, 85),
    ]

    # Decide on distractor object
    distractor_object = random.randint(1, 7)
    if distractor_object >= target_object:
        distractor_object += 1

    # Decide on distractor position
    if target_position == "left":
        distractor_position = "right"
        colour_positions = [target_colour, distractor_colour]
        orientation_positions = [target_orientation, distractor_orientation]
        object_positions = [target_object, distractor_object]
    elif target_position == "right":
        distractor_position = "left"
        colour_positions = [distractor_colour, target_colour]
        orientation_positions = [distractor_orientation, target_orientation]
        object_positions = [distractor_object, target_object]

    return {
        "ITI": random.randint(500, 800),
        "object_ids": object_positions,
        "orientations": orientation_positions,
        "colours": colour_positions,
        "target_object": target_object,
        "target_position": target_position,
        "target_orientation": target_orientation,
        "target_colour": target_colour,
        "distractor_object": distractor_object,
        "distractor_position": distractor_position,
        "distractor_orientation": distractor_orientation,
        "distractor_colour": distractor_colour,
    }


def do_while_showing(waiting_time, something_to_do, window):
    """
    Show whatever is drawn to the screen for exactly `waiting_time` period,
    while doing `something_to_do` in the mean time.
    """
    window.flip()
    start = time()
    something_to_do()
    wait(waiting_time - (time() - start))


def single_trial(
    ITI,
    object_ids,
    orientations,
    colours,
    target_object,
    target_position,
    target_orientation,
    target_colour,
    distractor_object,
    distractor_position,
    distractor_orientation,
    distractor_colour,
    stimuli,
    settings,
    testing,
    eyetracker=None,
):
    # Initial fixation cross to eliminate jitter caused by for loop
    draw_fixation_dot(stimuli["fixation_dot"])

    screens = [
        (0, lambda: 0 / 0, None),  # initial one to make life easier
        (ITI / 1000, lambda: draw_fixation_dot(stimuli["fixation_dot"]), None),
        (
            0.25,
            lambda: create_stimuli_frame(stimuli, object_ids, orientations, colours, settings),
            "stimuli_onset",
        ),
        (0.75, lambda: draw_fixation_dot(stimuli["fixation_dot"]), None),
        (1.5, lambda: draw_fixation_dot(stimuli["fixation_dot"], target_colour), "cue_onset"),
        (0.0, lambda: create_probe_cue_frame(stimuli, target_colour), None),
    ]

    # !!! The timing you pass to do_while_showing is the timing for the previously drawn screen. !!!
    for index, (duration, _, frame) in enumerate(screens[:-1]):
        # Send trigger if not testing
        if not testing and frame:
            trigger = get_trigger(frame, target_position, target_object)
            eyetracker.tracker.send_message(f"trig{trigger}")

        # Check for pressed 'q'
        check_quit(settings["keyboard"])

        # Draw the next screen while showing the current one
        do_while_showing(duration, screens[index + 1][1], settings["window"])

    # The for loop only draws the last frame, never shows it
    # So show it here
    settings["window"].flip()

    response = get_response(
        stimuli,
        target_position,
        target_object,
        target_orientation,
        target_colour,
        settings,
        testing,
        eyetracker,
        additional_objects=[],
    )

    # Show performance (and feedback on premature key usage if necessary)
    draw_fixation_dot(stimuli["fixation_dot"])
    show_text(response["performance"], settings["window"], (0, settings["deg2pix"](0.3)))

    if response["premature_pressed"] == True:
        show_text("!", settings["window"], (0, -settings["deg2pix"](0.3)))

    settings["window"].flip()
    sleep(0.25)

    return {
        "condition_code": get_trigger(
            "stimuli_onset",
            target_position,
            target_object,
        ),
        **response,
    }
