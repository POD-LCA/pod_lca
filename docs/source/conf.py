# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
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
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'geopy': ('https://geopy.readthedocs.io/en/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    'numpy': ('https://numpy.org/doc/stable/', None)
}

templates_path = ['_templates']
exclude_patterns = []
autodoc_member_order = 'bysource'

language = 'Python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme =  'piccolo_theme'  # https://piccolo-theme.readthedocs.io/en/latest/index.html
html_static_path = ['../_static']

# -- For gitbook markdown- ---------------------------------------------------
def add_gitbook_prefix(app, exception):
    if exception:
        return
    
    if app.builder.name != "markdown":
        return 
    
    group_prefix = "api-documentation/"  # your GitBook group name
    build_dir = app.outdir

    for root, _, files in os.walk(build_dir):
        for f in files:
            if f.endswith(".md"):
                path = os.path.join(root, f)
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()

                text = re.sub(r"\((?!https?:)([^)]+)\.md\)", rf"({group_prefix}\1)", text)

                # # 1. Add .md to any local links missing it (e.g. (api-documentation/electricity-generation))
                # text = re.sub(
                #     r"\((?!https?:)(?!/)([^)]+?)(?<!\.md)(?<!/)\)",
                #     r"(\1.md)",
                #     text
                # )

                # # 2️. Add prefix to .md links (but skip anchors)
                # text = re.sub(
                #     r"\((?!https?:)([^)#]+)\.md\)",
                #     rf"({group_prefix}\1)",
                #     text
                # )

                # # 3️. Leave anchor links (page.md#anchor) untouched
                # text = re.sub(
                #     r"\((?!https?:)([^)#]+)\.md(#.*?)\)",
                #     r"(\1\2)",
                #     text
                # )

                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)

def setup(app):
    app.connect("build-finished", add_gitbook_prefix)
