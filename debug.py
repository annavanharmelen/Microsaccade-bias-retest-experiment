"""
This script is used to test random aspects
of the 'microsaccade bias retest' experiment.

made by Anna van Harmelen, 2026
"""

from block import fixational_period
from set_up import get_monitor_and_dir, get_settings
from stimuli import initialise_all_stimuli
from psychopy import core, visual
from trial import generate_trial_characteristics

monitor, directory, stimuli_directory = get_monitor_and_dir(True)
settings = get_settings(monitor, directory)
stimuli = initialise_all_stimuli(stimuli_directory, settings)

fixational_period(0.05, stimuli["fixation_dot"], settings, None)
