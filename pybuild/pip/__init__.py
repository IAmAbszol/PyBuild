"""Handles everything that is pip inside PybBuild.

    This script supports installations required in PyBuild, specified either by the package itself
    or an outside developer seeking to install additional dependencies without having to communicate
    directly to Python itself, meaning, this acts as a wrapper around the process.

    Basic Usage:
    
    ```
    from pybuild import pip

    pip.install(env, 'pandas', user=False)
    ```
    
    The above will install the pandas package and the developer has requred to not install with user flag enabled.

"""
import logging

from pathlib import Path
from typing import List, Union

# from pybuild.environment import Environment
from pybuild.utils import process_utils


class Package:
    """Package class handles generics."""
    def __init__(self, package : str, version : str = None):
        """Initialization function of the class.

        Args:
            package: Package name.
            version: Version of package to install, example >=16.
        """
        self._package = package
        self._version = version


    def __str__(self):
        base_package = self._package
        if self._version:
            if '=' in self._version:
                base_package += self._version
            else:
                base_package += f'=={self._version}'
        return base_package


def freeze(environment, file_name : str) -> Path:
    """Freezes the pip dependencies of the current environment into a text file.

    Args:
        environment: Environment where PyBuild exists, this was initialized during the Environment initialization stage.
        file_name: File name to store the dependencies in.

    Returns:
        Path to file created through pip freeze.

    Raises:
        ValueError: Raised when process fails to execute properly.
        FileNotFoundError: Raised when pip freeze successfully runs but the file_name cannot be found.
    """
    rc = process_utils.create_process(str(environment.python()), f'-m pip freeze > {file_name}')
    if rc != 0:
        raise ValueError('Failed to freeze pip environment.')
    path = Path(Path.cwd(), file_name)
    if not path.exists():
        raise FileNotFoundError(f'Failed to find or create {file_name}.')
    return path


def install(environment, *packages : Union[Package, str], **kwargs) -> Union[Path, List[Path]]:
    """Installs packages for PyBuild environment.

    PyBuild allows the user to install packages on the fly by adding a wrapper around the pip command line.

    Args:
        environment: Environment where PyBuild exists, this was initialized during the Environment initialization stage.
        packages: Package to be installed, also supports multiple packages to be installed in the order provided.
        user: Enable the --user flag when calling pip from the command line. In most cases this should be True, especially on *nix systems.

    Returns:
        Return code of process launched.

    Raises:
        ValueError: Raised when process fails to execute properly.
    """
    # TODO: Process user input
    command_string = []
    for k, v in kwargs.items():
        processed_k = k.replace('_', '-')
        if str(v) == 'True':
            command_string.append('--{}'.format(processed_k))
        elif str(v) != 'False':
            command_string.append('--{} {}'.format(processed_k, v))

    rc = process_utils.create_process(str(environment.python()), '-m pip install {} {}'.format(' '.join(map(str, packages)) if packages else '', ' '.join(command_string)))
    if rc != 0:
        raise ValueError('Failed to install.')
    logging.info(f'Successfully installed {", ".join(map(str, packages))}.')
    return rc


def list(environment):# -> List[str]:
    """List packages for PyBuild environment.

    PyBuild allows the user to list packages from the environment by wrapping around pip through command line.

    Args:
        environment: Environment where PyBuild exists, this was initialized during the Environment initialization stage.

    Returns:
        TODO: Return list of strings. process_utils.create_process only prints to screen and doesn't allow for collection
                to happen outright.

    Raises:
        ValueError: Raised when process fails to execute properly.
    """
    rc = process_utils.create_process(str(environment.python()), '-m pip list')
    if rc != 0:
        raise ValueError('Failed to uninstall.')


def uninstall(environment, *packages : Union[Package, str], **kwargs) -> bool:
    """Uninstall packages for PyBuild environment.

    PyBuild allows the user to uninstall packages from the environment.

    Args:
        environment: Environment where PyBuild exists, this was initialized during the Environment initialization stage.
        packages: Package to be uninstalled, also supports multiple packages to be uninstalled in the order provided.

    Returns:
        True if all the packages were removed successfully else False.

    Raises:
        ValueError: Raised when process fails to execute properly.
    """
    command_string = []
    for k, v in kwargs.items():
        processed_k = k.replace('_', '-')
        if str(v) == 'True':
            command_string.append('--{}'.format(processed_k))
        else:
            command_string.append('--{} {}'.format(processed_k, v))

    rc = process_utils.create_process(str(environment.python()), '-m pip uninstall -y {} {}'.format(' '.join(map(str, packages)) if packages else '', ' '.join(command_string)))
    if rc != 0:
        raise ValueError('Failed to uninstall.')
    logging.info(f'Successfully uninstalled {", ".join(map(str, packages))}.')
    return rc


def upgrade(environment, *packages : Package) -> bool:
    """Upgrades package to latest.

    PyBuild allows the user to upgrade packages from the environment.

    Args:
        environment: Environment where PyBuild exists, this was initialized during the Environment initialization stage.
        packages: Package to be upgraded, also supports multiple packages to be installed in the order provided.

    Returns:
        True if all the packages were upgraded successfully else False.

    Raises:
        ValueError: Raised when process fails to execute properly.
    """
    rc = process_utils.create_process(str(environment.python()), '-m pip -U {}'.format(' '.join(map(str, packages)) if packages else ''))
    if rc != 0:
        raise ValueError('Failed to upgrade.')
    logging.info(f'Successfully upgraded {", ".join(map(str, packages))}.')
    return rc