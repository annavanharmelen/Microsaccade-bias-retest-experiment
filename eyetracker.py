"""
This file contains the functions necessary for
connecting and using the eyetracker.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2026, using code by Ezra Nasrawi & Baiwei Liu
"""

from lib import eyelinker
from psychopy import event
import os


class Eyelinker:
    """
    usage:

       from eyetracker import Eyelinker

    To initialise:

       eyelinker = Eyelinker(participant, session, window, directory)
       eyelinker.calibrate()
    """

    def __init__(self, participant, session, window, directory) -> None:
        """
        This also connects to the tracker
        """
        self.directory = directory
        self.window = window
        self.tracker = eyelinker.EyeLinker(
            window=window, eye="RIGHT", filename=f"{session}_{participant}.edf"
        )
        self.tracker.init_tracker()

    def start(self):
        self.tracker.start_recording()

    def calibrate(self):
        self.tracker.calibrate()

    def stop(self):
        os.chdir(self.directory)

        self.tracker.stop_recording()
        self.tracker.transfer_edf()
        self.tracker.close_edf()


def get_trigger(frame, target_position, target_object):
    condition_marker = target_object

    if target_position == "right":
        condition_marker += 8

    return {
        "stimuli_onset": "1",
        "cue_onset": "2",
        "response_onset": "3",
        "response_offset": "4",
        "feedback_onset": "5",
    }[frame] + str(condition_marker)
