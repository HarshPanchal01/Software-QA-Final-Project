from enum import Enum
"""
    src/shared/models.py

    Data classes shared between the frontend and backend

    Data classes:
        - MessageType: helper for frontend visuals
"""

class MessageType(Enum):
    """
    Enumeration for Message Types in the CLI.
    
    Intention:
        Standardizes the types of messages that can be printed to the console (Error, Success, Info, Warning)
        and associates them with specific colors for better user experience.
    """
    ERROR = 'red'
    SUCCESS = 'green'
    ACTION = 'cyan'
    INFO = 'gray'
    WARNING = 'yellow'
    NORMAL = 'white'
