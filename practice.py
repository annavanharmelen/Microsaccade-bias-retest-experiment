"""
This file contains the functions necessary for
practising the trials and the use of the report dial.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

from trial import (
    single_trial,
    generate_trial_characteristics,
)
from stimuli import show_text, draw_fixation_dot, draw_one_object, create_probe_cue_frame
from response import get_response, wait_for_key, check_quit
from psychopy import core
from psychopy.hardware.keyboard import Keyboard
from trial import generate_trial_characteristics
from time import sleep
import random
from numpy import mean


def practice(stimuli, eyetracker, settings):
    # Practice response itself
    practice_response(stimuli, eyetracker, settings)

    # Practice full trials
    practice_trials(stimuli, eyetracker, settings)


def practice_response(stimuli, eyetracker, settings):
    # Practice response until participant chooses to stop
    try:
        performance = []

        # Show first screen
        show_text(
            "Welcome!"
            "\nPress SPACE to start practicing how to respond.",
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

        while True:
            # Show fixation dot in preparation
            draw_fixation_dot(stimuli["fixation_dot"])
            settings["window"].flip()
            sleep(0.5)

            # Generate random characteristics
            target_position = random.choice(["left", "right"])
            target_object = random.randint(1, 8)
            target = generate_trial_characteristics(target_object, target_position)
            target_orientation = target["target_orientation"]

            # Display object with a random orientation + probe wheel around it
            object = draw_one_object(
                stimuli["objects"][target_object],
                target_orientation,
                "#eaeaea",
                "middle",
                settings,
            )
            create_probe_cue_frame(stimuli, "#eaeaea")
            settings["window"].flip()

            # Allow response
            report = get_response(
                stimuli,
                target_position,
                target_object,
                target_orientation,
                None,
                settings,
                True,
                None,
                [object],
            )

            # Save for post-hoc feedback
            performance.append(int(report["performance"]))

            # Show feedback
            draw_fixation_dot(stimuli["fixation_dot"])
            show_text(
                f"{report['performance']}",
                settings["window"],
                (0, settings["deg2pix"](0.3)),
            )

            if report["premature_pressed"] == True:
                show_text("!", settings["window"], (0, -settings["deg2pix"](0.3)))

            settings["window"].flip()
            sleep(0.25)

            # Pause before next one
            draw_fixation_dot(stimuli["fixation_dot"])
            settings["window"].flip()
            sleep(random.randint(500, 800) / 1000)

            # Check for pressed 'q'
            check_quit(settings["keyboard"])

    except KeyboardInterrupt:
        if len(performance) > 0:
            avg_score = round(mean(performance), 1)
            show_text(
                f"During this practice, your average score was: {avg_score}"
                "\n\nPress SPACE to start practicing the task.",
                settings["window"],
            )
        else:
            show_text(
                "You skipped practice 1.\n\nPress SPACE to start practicing the task.",
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

        # Make sure the keystroke from moving to the next part isn't saved
        settings["keyboard"].clearEvents()


def practice_trials(stimuli, eyetracker, settings):
    # Practice full trials until participant chooses to stop
    try:
        performance = []

        while True:
            target_position = random.choice(["left", "right"])
            target_object = random.randint(1, 8)
            trial_characteristics = generate_trial_characteristics(target_object, target_position)

            # Generate trial
            report = single_trial(
                **trial_characteristics,
                stimuli=stimuli,
                settings=settings,
                testing=True,
                eyetracker=None,
            )

            # Save for feedback
            performance.append(int(report["performance"]))

    except KeyboardInterrupt:
        settings["window"].flip()
        if len(performance) > 0:
            avg_score = round(mean(performance), 1)
            show_text(
                f"During this practice, your average score was: {avg_score}"
                "\n\nPress SPACE to start the experiment.",
                settings["window"],
            )
        else:
            show_text(
                "You skipped practice 2.\n\nPress SPACE to start the experiment.",
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
