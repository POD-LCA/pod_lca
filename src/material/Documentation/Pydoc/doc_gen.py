import os
import subprocess
import shutil

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

def generate_docs(package_dir, package_name="", ignore=[]):
    working_directory = os.path.join(package_dir, '..')
    for root, dirs, files in os.walk(package_dir):
        for folder in ignore:
            folder_path = HOME + folder
            if root == folder_path:
                continue

        if "__init__.py" not in files:
            continue

        package_path = root.replace(package_dir, "").replace(os.sep, ".").strip(".")
        if package_name:
            package_path = f"{package_name}.{package_path}" if package_path else package_name

        if package_path:
            subprocess.run(["python", "-m", "pydoc", "-w", package_path], shell=True, cwd=working_directory)
            shutil.move(f"{working_directory}\\{package_path}.html", 
                        f"{package_dir}\\Documentation\\{package_path}.html")

        for file in files:
            if file in ignore:
                continue
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]  # Remove the .py extension
                full_module_name = f"{package_path}.{module_name}" if package_path else module_name
                subprocess.run(["python", "-m", "pydoc", "-w", full_module_name], shell=True, cwd=working_directory)
                shutil.move(f"{working_directory}\\{package_path}.{module_name}.html", 
                            f"{package_dir}\\Documentation\\\\{package_path}.{module_name}.html")

if __name__ == '__main__':
    from material import HOME
    generate_docs(HOME, "material", ignore=['\\Documenetation', 'unit_tests.py'])

# themes