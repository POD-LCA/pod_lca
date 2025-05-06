
import yaml


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


def load_config():
    """  Load the configuration file.
    """
    path = 'config.yaml'
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = load_config()
