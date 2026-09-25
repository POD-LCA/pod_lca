from invoke import task
from invoke.exceptions import UnexpectedExit
from pathlib import Path
from shutil import rmtree
import importlib.util
import inspect
import os
import sys


@task
def clean(c):
    """Clean all generated artifacts."""
    dirs_to_remove = ["build", "dist", ".pytest_cache", "docs/_build"]

    for d in dirs_to_remove:
        if os.path.isdir(d):
            rmtree(d)
            print(f"Removed directory: {d}")

    for pycache in Path(".").rglob("__pycache__"):
        rmtree(pycache)
        print(f"Removed: {pycache}")

    for pyc in Path(".").rglob("*.pyc"):
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
    failures = []
    commands = ["black . --check", "ruff check .", "mypy src", "pydocstyle src --convention=numpy"]

    for cmd in commands:
        print(f"\nRunning: {cmd}")
        try:
            c.run(cmd, echo=True)
        except UnexpectedExit:
            print(f"Failed: {cmd}")
            failures.append(cmd)

    if failures:
        print("\nSummary of failures:")
        for f in failures:
            print(" -", f)
    else:
        print("\nAll checks passed!")


@task
def fix(c):
    """Fix code formatting using Black (formatting) and Ruff (linting)"""
    commands = ["black .", "ruff check . --fix"]

    for cmd in commands:
        print(f"Running: {cmd}")
        c.run(cmd, echo=True)

    print("All checks passed (or reported).")


@task
def docs(c, out="md"):
    """Build Sphinx docs"""
    if out == "html":
        c.run("sphinx-build -b html docs/source docs/_build/html")
    elif out == "md":
        c.run("sphinx-build -b markdown docs/source docs/_build/md")


def load_test_module(filepath):
    """Dynamically import a Python file as a module."""
    filepath = Path(filepath)
    spec = importlib.util.spec_from_file_location(filepath.stem, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

@task
def unittests(c, verbose=True):
    """Run unit tests in tests/unit_tests using pytest."""
    test_path = os.path.join("tests", "unit_tests")
    
    cmd = f"pytest {test_path}"
    if verbose:
        cmd += " -vv"
    
    if sys.platform == "win32":
        c.run(cmd)  
    else:
        c.run(cmd, pty=True)

@task
def tests(c):
    """Discover every *_test_script.py file, import it, and run its test_* functions."""
    test_files = list(Path("tests").rglob("*_test_script.py"))

    if not test_files:
        print("No test_script.py files found.")
        return

    total_passed = 0
    total_failed = 0
    for file in test_files:
        print(f"\n=== Running tests in {file} ===")
        module = load_test_module(file)

        for name, func in inspect.getmembers(module, inspect.isfunction):
            if name.startswith("test_"):
                print(f"Running {name}...")
                try:
                    func()
                except AssertionError:
                    total_failed += 1
                except Exception:
                    total_failed += 1
                else:
                    total_passed += 1

    print(f">>{total_passed} of {total_passed + total_failed} tests passed.")


@task(pre=[clean])
@task
def package(c, version_bump="patch"):
    """Build only the wheel.
    
    Parameters
    ----------
    version_bump : str
        One of 'major', 'minor', or 'patch' to indicate the type of version bump.
    """
    # c.run(f"bump-my-version bump {version_bump} ")
    c.run("python -m build --wheel")
