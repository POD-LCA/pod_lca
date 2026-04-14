__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from importlib import resources

import yaml


def load_config():
    """Load the configuration file."""
    with resources.open_text("pod_lca", "config.yaml") as f:
        config = yaml.safe_load(f)

    update_filepaths(config)

    return config


def update_filepaths(config):
    """Update file paths to absolute file path."""
    for group, paths_dict in config["file_paths"].items():
        for key, relative_path in paths_dict.items():
            target_node = resources.files("pod_lca")
            
            parts = relative_path.split('/')
            
            for part in parts:
                if part == "..":
                    target_node = target_node.parent
                elif part == "." or not part:
                    continue
                else:
                    target_node = target_node.joinpath(part)
            
            paths_dict[key] = target_node


config = load_config()
