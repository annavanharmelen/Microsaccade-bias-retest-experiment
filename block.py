"""
This file contains the functions necessary for
creating and running a full block of trials start-to-finish.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

import random
from stimuli import show_text, draw_fixation_dot
from response import wait_for_key
from psychopy import core

def create_trial_list(n_trials):
    if n_trials % 16 != 0:
        raise Exception(
            "Expected n_trials to be divisible by 16, otherwise perfect counterbalancing is not possible."
        )

    # Generate equal distribution target objects
    target_object = n_trials // 8 * list(range(1, 9, 1))

    # Generate equal distribution of target locations
    target_position = n_trials // 2 * ["left"] + n_trials // 2 * ["right"]

    # Create trial parameters for all trials
    trials = list(zip(target_object, target_position))
    random.shuffle(trials)

    return trials


def block_break(current_block, n_blocks, avg_score, settings, eyetracker):
    blocks_left = n_blocks - current_block

    show_text(
        f"On the previous block, your average score was: {avg_score}"
        f"\n\nYou just finished block {current_block}, you {'only ' if blocks_left == 1 else ''}"
        f"have {blocks_left} block{'s' if blocks_left != 1 else ''} left. "
        "Take a break if you want to, but try not to move your head during this break."
        "\n\nPress SPACE when you're ready to continue.",
        settings["window"],
    )
    settings["window"].flip()

    if eyetracker:
        keys = wait_for_key(["space", "c"], settings["keyboard"])
        if "c" in keys:
            eyetracker.calibrate()
            eyetracker.start()
            return True
    else:
        wait_for_key(["space"], settings["keyboard"])

    # Make sure the keystroke from starting the experiment isn't saved
    settings["keyboard"].clearEvents()

    return False


def long_break(n_blocks, avg_score, settings, eyetracker):
    show_text(
        f"On the previous block, your average score was: {avg_score}"
        f"\n\nYou're halfway through! You have {n_blocks // 2} blocks left. "
        "Now is the time to take a longer break. Maybe get up, stretch, walk around."
        "\n\nPress SPACE whenever you're ready to continue.",
        settings["window"],
    )
    settings["window"].flip()

    if eyetracker:
        keys = wait_for_key(["space", "c"], settings["keyboard"])
        if "c" in keys:
            eyetracker.calibrate()
            return True
    else:
        wait_for_key(["space"], settings["keyboard"])

    # Make sure the keystroke from starting the experiment isn't saved
    settings["keyboard"].clearEvents()

    return False

def fixational_period(duration, dot_item, settings, eyetracker):
    while True:
        # Start
        show_text(
            f"Please fixate on the following dot for {duration} minutes."
            f"\nYou will start with {duration / 2} minutes, and then get a break before continuing."
            "\n\nPress SPACE to start",
            settings["window"],
        )
        settings["window"].flip()

        # Wait for key press
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
            elif "space" in keys:
                break
        else:
            wait_for_key(["space"], settings["keyboard"])
            break

    # Fixate in 2 parts, with a small break in between
    fixate(duration / 2, dot_item, settings, eyetracker)

    while True:
        show_text(
            "That was the first half! Give your eyes a rest for as long as you want."
            f"\n\nPress SPACE to fixate for the final {duration / 2} minutes.",
            settings["window"],
        )
        settings["window"].flip()

        # Wait for key press
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
            elif "space" in keys:
                break
        else:
            wait_for_key(["space"], settings["keyboard"])
            break

    fixate(duration / 2, dot_item, settings, eyetracker)
        
    # End
    while True:
        show_text(
            "That was it! Thanks for fixating!"
            "\n\nPress SPACE to start the second half of the experiment",
            settings["window"],
        )
        settings["window"].flip()

        # Wait for key press
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
            elif "space" in keys:
                break
        else:
            wait_for_key(["space"], settings["keyboard"])
            break

def fixate(duration, dot_item, settings, eyetracker):
    draw_fixation_dot(dot_item)
    settings["window"].flip()
    
    if eyetracker:
        eyetracker.tracker.send_message(f"trig{1000}")

    core.wait(duration * 60)

    if eyetracker:
        eyetracker.tracker.send_message(f"trig{2000}")

def finish(n_blocks, settings):
    show_text(
        f"Congratulations! You successfully finished all {n_blocks} blocks!"
        "You're completely done now. Press SPACE to exit the experiment.",
        settings["window"],
    )
    settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])


def quick_finish(settings):
    settings["window"].flip()
    show_text(
        f"You've exited the experiment. Press SPACE to close this window.",
        settings["window"],
    )
    settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])
