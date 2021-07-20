"""Creates Python executable inside the provided environment.

    PyBuild supports the developer in building an executable
    of either their entire program or specific modules for said program,
    configurability is everything.

    Basic Usage:

"""
import logging

from pybuild import pip
from pybuild.environment import Environment
from pybuild.utils import process_utils


def make_executable(environment : Environment, command : str) -> int:
    """Creates the executable using PyInstaller.

    PyInstaller creates executable binaries for Windows, Linux, and macOS. The arguments provided must match what's passed 
    to PyInstaller command, later this function will be refined.

    Args:
        environment: Environment where PyBuild exists, this was initialized during the Environment initialization stage.
        command: Command to pass to PyInstaller.
    
    Returns:
        Return code of the subprocess executed with PyInstaller.
    """
    if environment.dependency_exists('pyinstaller') is None:
        pip.install(environment, 'pyinstaller')
    pyinstaller_executable = [x for x in environment.executables() if 'pyinstaller' in x.name][0]
    return process_utils.create_process(str(pyinstaller_executable), command)