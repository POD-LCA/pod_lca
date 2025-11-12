
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pathlib import Path

import yaml

def load_config():
    """  Load the configuration file.
    """
    path = Path(__file__).resolve().parents[3] / 'config.yaml'
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    
    update_filepaths(config, parent_level=3)

    return config

def update_filepaths(config, parent_level=1):
    """ Update file paths to absolute file path.
    """
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[parent_level]
    for group, paths_dict in config['file_paths'].items():
        for key, path in paths_dict.items():
            paths_dict[key] = project_root / path

config = load_config()
