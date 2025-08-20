# POD-LCA

Python Library for Parametric and Dynamic LCA


## Getting started with this project

### Setup code editor

1. Open project folder in VS Code
2. Select python environment for the project
3. First time using VS Code and on Windows? Make sure select the correct terminal profile: `Ctrl+Shift+P`, `Terminal: Select Default Profile` and select `Command Prompt`.

> All terminal commands in the following sections can be run from the VS Code integrated terminal. 


### First steps with git

1. Go to the `Source control` tab
2. Make an initial commit with all newly created files


### First steps with code

1. Install the newly created project 

        pip install -e .

### Code conventions

To be updated...
<!-- Code convention follows [PEP8](https://pep8.org/) style guidelines and line length of 120 characters.

1. Check adherence to style guidelines

        invoke lint

2. Format code automatically

        invoke format -->


### Documentation

Documentation is generated automatically out of docstrings and [RST](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) files in this repository

1. Generate the docs

        invoke docs

2. Open docs in your browser (file explorer -> `pod_lca/docs/source docs/_build/html/index.html`)


### Testing

Tests are written using the [pytest](https://docs.pytest.org/) framework

1. Run all tests from terminal

        invoke tests


### Publish release

To be updated...
<!-- Releases follow the [semver](https://semver.org/spec/v2.0.0.html) versioning convention.

1. Create a new release

        invoke release major -->
