
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..utilities import config

LOG_LEVELS = {
                "Fatal": 0,
                "Error": 1,
                "Warn": 2,
                "Info": 3,
                "Debug": 4,
                "Trace": 5
            }

def log(str, level="Info"):
    """ Log messages to the console bvased on the log level set.

    Parameters
    ----------
    str : str
        The message to log.
    level : str, optional
        The log level of the message. The default is 0.
            #   Log Level	Importance
            0   Fatal	One or more key business functionalities are not working and the whole system doesn’t fulfill the business functionalities.
            1   Error	One or more functionalities are not working, preventing some functionalities from working correctly.
            2   Warn	Unexpected behavior happened inside the application, but it is continuing its work and the key business features are operating as expected.
            3   Info	An event happened, the event is purely informative and can be ignored during normal operations.
            4   Debug	A log level used for events considered to be useful during software debugging when more granular information is needed.
            5   Trace	A log level describing events showing step by step execution of your code that can be ignored during the standard operation, but may be useful during extended debugging sessions.
    """
    if LOG_LEVELS[config['setup']['utilities']['LOG_LEVEL']] >= LOG_LEVELS[level]:
        tabs = '>' * (LOG_LEVELS[level])
        print(f"{tabs}{str}")
