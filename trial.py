"""
This file contains the functions necessary for
creating and running a single trial start-to-finish,
including eyetracker triggers.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import visual
from psychopy.core import wait
from time import time, sleep
from response import get_response, check_quit
from stimuli import (
    create_fixation_dot,
    create_stimuli_frame,
)
from eyetracker import get_trigger
import random

# COLOURS = blue, pink, green, orange
COLOURS = [
    [(rgb_value / 128 - 1) for rgb_value in rgb_triplet]
    for rgb_triplet in [[19, 146, 206], [217, 103, 241], [101, 148, 14], [238, 104, 60]]
]

def generate_trial_characteristics():
    # Decide on random colours of stimulus
    stimuli_colours = random.sample(COLOURS, 2)

    # Create random stimuli orientations
    orientations = [
        random.choice([-1, 1]) * random.randint(5, 85),
        random.choice([-1, 1]) * random.randint(5, 85),
    ]

    # TODO
    ...

    return {
        "ITI": random.randint(500, 800),
        "stimuli_colours": stimuli_colours,
        "trial_condition": condition,
        "left_orientation": orientations[0],
        "right_orientation": orientations[1],
        "target_bar": target_bar,
        "target_colour": target_colour,
        "target_orientation": ...,
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
    static_duration,
    ITI,
    change_direction,
    left_orientation,
    right_orientation,
    left_orientation_2,
    right_orientation_2,
    target_bar,
    target_colour,
    target_pre_orientation,
    target_post_orientation,
    stimuli_colours,
    capture_colour,
    trial_condition,
    stimuli,
    settings,
    testing,
    eyetracker=None,
):
    # Initial fixation cross to eliminate jitter caused by for loop
    create_fixation_dot(settings)

    screens = [
        (0, lambda: 0 / 0, None),  # initial one to make life easier
        (ITI / 1000, lambda: create_fixation_dot(settings), None),
        (
            0.75,
            lambda: create_stimuli_frame(
                left_orientation, right_orientation, stimuli_colours, settings
            ),
            "stimuli_onset",
        ),
        (
            static_duration / 1000,
            lambda: create_stimuli_frame(
                left_orientation,
                right_orientation,
                stimuli_colours,
                settings,
                capture_colour,
            ),
            "cue_onset",
        ),
        (
            None,
            lambda: create_stimuli_frame(
                left_orientation_2,
                right_orientation_2,
                stimuli_colours,
                settings,
                capture_colour,
            ),
        ),
    ]

    # !!! The timing you pass to do_while_showing is the timing for the previously drawn screen. !!!
    for index, (duration, _, frame) in enumerate(screens[:-1]):
        # Send trigger if not testing
        if not testing and frame:
            trigger = get_trigger(frame, trial_condition, target_bar, change_direction)
            eyetracker.tracker.send_message(f"trig{trigger}")

        # Check for pressed 'q'
        check_quit(settings["keyboard"])

        # Draw the next screen while showing the current one
        do_while_showing(duration, screens[index + 1][1], settings["window"])

    # The for loop only draws the last frame, never shows it
    # So show it here
    if not testing:
        trigger = get_trigger(
            "orientation_change", trial_condition, target_bar, change_direction
        )
        eyetracker.tracker.send_message(f"trig{trigger}")

    settings["window"].flip()

    response = get_response(
        settings,
        testing,
        eyetracker,
        trial_condition,
        change_direction,
        target_bar,
    )

    # Show performance (and feedback on premature key usage if necessary)
    create_fixation_dot(settings)
    show_text(response["feedback"], settings["window"], (0, settings["deg2pix"](0.3)))

    if response["premature_pressed"] == True:
        show_text("!", settings["window"], (0, -settings["deg2pix"](0.3)))

    settings["window"].flip()
    sleep(0.25)

    return {
        "condition_code": get_trigger(
            "stimuli_onset", trial_condition, target_bar, change_direction
        ),
        **response,
    }
