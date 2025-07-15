# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'POD|LCA Python Framework'
copyright = '2025, POD LCA Team'
author = 'POD LCA Team'
release = 'v0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.napoleon', 'sphinx.ext.intersphinx']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None)
}

templates_path = ['_templates']
exclude_patterns = []
autodoc_member_order = 'bysource'

language = 'Python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'piccolo_theme'  # https://piccolo-theme.readthedocs.io/en/latest/index.html
html_static_path = ['../_static']
