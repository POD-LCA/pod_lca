
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from importlib import resources

import yaml

def load_config():
    """  Load the configuration file.
    """
    with resources.open_text("pod_lca", "config.yaml") as f:
        config = yaml.safe_load(f)
    
    update_filepaths(config)

    return config

def update_filepaths(config):
    """ Update file paths to absolute file path.
    """
    for group, paths_dict in config['file_paths'].items():
        for key, relative_path in paths_dict.items():
            package_root = resources.files("pod_lca")
            file_path = package_root.joinpath(relative_path)
            paths_dict[key] = file_path

config = load_config()
