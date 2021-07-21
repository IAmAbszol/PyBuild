"""Virtual Environment class that handles installation designated by the user.

    A user may want to install additional dependencies to their base system Python or the Python the ran PyBuild with, effectively being
    regarded as the systems interpreter. In the event of this, VirtualEnv was stood up to allow the user freedom of creating a virtual environment
    whenever and allowing themselves to install dependencies using pip prior to the virtual environments creation.

    Environment has a hard set limitation based on _find_interpreter that only runs once, after the sys.executable and __interpreter differ
    the function won't operate again. To avoid this, create multiple environments where you need additional virtual environments.

    Basic Usage:
    with Environment('pybuildenv') as environment:
        virtual_environment_pkg = VirtualEnv(environment)
        ...

        second_environment = Environment('testenv')
        virtual_environment_pkg = VirtualEnv(second_environment)
        ...
        second_environment.cleanup()

    The return value of VirtualEnv is typically useless. Packages currently are only used for displaying the package and version in a way for pip to understand.

"""
from pathlib import Path

from pybuild import pip
from pybuild.environment import Environment
from pybuild.utils import os_utils, process_utils


class VirtualEnv(pip.Package):
    """Virtual Environment Class."""
    def __init__(self, environment : Environment, version : str = None, user : bool = False, clean : bool = False):
        """Virtual Environment initialization function.

        Args:
            environment: Environment to use for VirtualEnv creation.
            version: Version of virtualenv to install.
            user: virtualenv package should be installed as user.
            clean: Clean the virtual environment off the system prior to creating a new one, happens if the same virtual environment exists.
        """
        super().__init__('virtualenv', version=version)
        
        if environment.dependency_exists('virtualenv') == (None, None):
            pip.install(environment, self, user=user)
        venv_path = Path(environment.name())
        if venv_path.exists() and clean:
            os_utils.remove_directory(environment.name())
        if process_utils.create_process(str(environment.python()), f'-m virtualenv {environment.name()}') != 0:
            raise OSError('Failed to create virtual environment.')
        environment._find_interpreter()

