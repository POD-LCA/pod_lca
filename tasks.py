import os
import pathlib
import shutil
from invoke import task


@task
def clean(c):
    """Clean all generated artifacts."""
    dirs_to_remove = ["build", "dist", ".pytest_cache", "docs/_build"]

    for d in dirs_to_remove:
        if os.path.isdir(d):
            shutil.rmtree(d)
            print(f"Removed directory: {d}")

    for pycache in pathlib.Path(".").rglob("__pycache__"):
        shutil.rmtree(pycache)
        print(f"Removed: {pycache}")

    for pyc in pathlib.Path(".").rglob("*.pyc"):
        pyc.unlink()
        print(f"Removed: {pyc}")

    print("Clean complete.")


@task
def check(c):
    """Run various code and documentation style checks.

    This includes:
    - Black (formatting check)
    - Ruff (linting)
    - MyPy (static type checking)
    - Docstring (documentation linting)
    """
    commands = ["black check .", "ruff check .", "mypy src", "pydocstyle src --convention=numpy"]

    for cmd in commands:
        print(f"Running: {cmd}")
        c.run(cmd, echo=True)

    print("All checks passed (or reported).")


@task
def fix(c):
    """Run various code and documentation style checks.

    This includes:
    - Black (formatting check)
    - Ruff (linting)
    - MyPy (static type checking)
    - Docstring (documentation linting)
    """
    commands = ["black .", "ruff --fix .", "mypy src", "pydocstyle src --convention=numpy"]

    for cmd in commands:
        print(f"Running: {cmd}")
        c.run(cmd, echo=True)

    print("All checks passed (or reported).")


@task
def docs(c, out="md"):
    """Build Sphinx HTML docs"""
    if out == "html":
        c.run("sphinx-build -b html docs/source docs/_build/html")
    elif out == "md":
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


@task(pre=[clean])
@task
def package(c):
    """Build only the wheel."""
    c.run("python -m build --wheel")


# * `invoke clean`: Clean all generated artifacts.
# * `invoke check`: Run various code and documentation style checks.
# * `invoke docs`: Generate documentation.
# * `invoke test`: Run all tests and checks in one swift command.
