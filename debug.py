"""
This script is used to test random aspects
of the 'microsaccade bias retest' experiment.

made by Anna van Harmelen, 2026
"""

from block import fixational_period
from set_up import get_monitor_and_dir, get_settings
from stimuli import initialise_all_stimuli

monitor, dir = get_monitor_and_dir(True)
settings = get_settings(monitor, dir)

stimuli = initialise_all_stimuli(settings)

fixational_period(5, stimuli["fixation_dot"], settings, None)
