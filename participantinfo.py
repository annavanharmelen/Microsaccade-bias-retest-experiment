"""
This file contains the functions necessary for
collecting participant data.
To run the 'microsaccade bias retest' experiment, see main.py.

made by Anna van Harmelen, 2026
"""

import random
import pandas as pd


def get_participant_details(existing_participants: pd.DataFrame, testing):
    # Check whether this is a participant's first session?
    first_session = input("First session (y/n)? ")

    if first_session.lower() == "y":
        current_session = 1
    else:
        current_session = 2
    
    # Ask for participant number (based on randomly generated list)
    participant = int(input("Participant number: "))

    if not testing:
        # Get participant age
        age = int(input("Participant age: "))
    else:
        age = 00

    # Insert session number
    session = max(existing_participants.session_number) + 1

    new_participant = pd.DataFrame(
        {
            "participant_number": [participant],
            "session_number": [session],
            "session_within_pp": [current_session],
            "age": [age],
        }
    )
    all_participants = pd.concat(
        [existing_participants, new_participant], ignore_index=True
    )

    return all_participants, current_session
