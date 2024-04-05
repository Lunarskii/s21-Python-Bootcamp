from enum import Enum


"""
The module 'personality.py ' contains an enumeration of the personality type
"""


class PersonalityType(Enum):
    """
    The class contains an enumeration of personality types

    :cvar HUMAN: Human.
    :type HUMAN: PersonalityType

    :cvar REPLICANT: Replicant.
    :type REPLICANT: PersonalityType
    """

    HUMAN = 0
    REPLICANT = 1
