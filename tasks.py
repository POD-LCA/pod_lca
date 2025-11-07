
import pathlib
from invoke import task

@task
def docs(c, out='md'):
    """Build Sphinx HTML docs"""
    if out=='html':
        c.run("sphinx-build -b html docs/source docs/_build/html")
    elif out=='md':
        c.run("sphinx-build -b markdown docs/source docs/_build/md")

@task
def tests(c):
    """Run test files"""
    test_dir = pathlib.Path("tests")
    scripts = sorted(test_dir.glob("*_test_script.py"))

    if not scripts:
        print("No test scripts found.")
        return

    for script in scripts:
        print(f"Running {script}...")
        c.run(f"python {script}")
