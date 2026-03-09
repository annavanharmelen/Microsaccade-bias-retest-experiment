"""
This file contains the functions necessary for
practising the trials and the use of the report dial.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from trial import (
    single_trial,
    generate_trial_characteristics,
)
from stimuli import show_text
from response import get_response, wait_for_key, check_quit
from psychopy import event
from psychopy.hardware.keyboard import Keyboard
from trial import COLOURS
from time import sleep
import random
from numpy import mean

# 1. Practice giving a response to a single stimulus
# 2. Practice full trials


def practice(testing, settings):
    # Show explanation
    show_text(
        f"Welcome to the practice trials. You will practice each part until you press Q. \
            \n\nPress SPACE to start the practice session.",
        settings["window"],
    )
    settings["window"].flip()
    wait_for_key(["space"], settings["keyboard"])

    # Practice single stimulus until user chooses to stop
    try:
        while True:
            orientation = random.choice([-1, 1]) * random.randint(5, 85)
            new_orientation = orientation + random.choice([-1, 1]) * 5
            if new_orientation < orientation:
                change_direction = "anticlockwise"
            else:
                change_direction = "clockwise"

            colour = random.choice(COLOURS)

            make_one_gabor(orientation, colour, "middle", settings).draw()
            create_fixation_dot(settings)

            check_quit(settings["keyboard"])

            settings["window"].flip()
            sleep(random.randint(500, 1500) / 1000)

            make_one_gabor(new_orientation, colour, "middle", settings).draw()
            create_fixation_dot(settings)

            settings["window"].flip()
            response = get_response(
                settings, testing, None, "valid", change_direction, None
            )

            show_text(
                response["feedback"],
                settings["window"],
                (0, settings["deg2pix"](0.3)),
            )
            create_fixation_dot(settings)

            settings["window"].flip()
            sleep(0.5)

    except KeyboardInterrupt:
        settings["window"].flip()
        show_text(
            "You decided to stop practicing how to respond to the stimulus."
            "Press SPACE to start practicing full trials."
            "\n\nRemember to press Q to stop practising these trials once you feel comfortable starting the real experiment.",
            settings["window"],
        )
        settings["window"].flip()
        wait_for_key(["space"], settings["keyboard"])

    # Practice trials until user chooses to stop

    performance = []

    try:
        while True:
            orientation = random.choice([-1, 1]) * random.randint(5, 85)
            new_orientation = orientation + random.choice([-1, 1]) * 5
            if new_orientation < orientation:
                change_direction = "anticlockwise"
            else:
                change_direction = "clockwise"

            stimulus = generate_trial_characteristics(
                random.choice(8 * ["valid"] + 2 * ["invalid"]),
                random.choice(["left", "right"]),
                random.choice(list(range(500, 3201, 300))),
                change_direction,
            )

            report: dict = single_trial(**stimulus, settings=settings, testing=True)

            performance.append(report["correct_key"])

    except KeyboardInterrupt:
        settings["window"].flip()
        show_text(
            f"You decided to stop practicing. "
            f"\nDuring this practice, you answered correctly {round(mean(performance) * 100) if performance else 0}% of the time."
            "\n\nPress SPACE to start the experiment.",
            settings["window"],
        )
        settings["window"].flip()

    wait_for_key(["space"], settings["keyboard"])

    # Make sure the keystroke from starting the experiment isn't saved
    settings["keyboard"].clearEvents()
