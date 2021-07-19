"""Environment prepares a virtual environment for the PyBuild to run within.

    Every process in PyBuild requires a virtual environment to run inside to avoid any conflict
    with a cleaned system Python.

    Basic Usage:

    ```environment = Environment('pybuildenv')```

    ```with``` is available and easy to use with cleanup on ```exit```.

    ```
    with Environment('pybuildenv') as environment:
        pass
    ```
"""
import logging
import pathlib
import os
import struct
import sys

from tempfile import NamedTemporaryFile
from typing import List, Tuple, Union

from pybuild import pip
from pybuild.utils import file_utils, os_utils, process_utils

# TODO: Create snapshot=False argument where the environment
# is saved and later restored after with context completes or
# __del__ occurs.
class Environment:

    def __init__(self, env_name : str):
        """Creates an Environment for PyBuild to run in.

        Environment initialization function.

        Args:
            env_name Environment name to operate in.
        """
        assert isinstance(env_name, str)
        self.__interpreter = pathlib.Path(sys.executable)
        self.__env_name = env_name
        self.__environment_path = pathlib.Path(env_name)

        # Setup basic logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__environment_path.exists():
            os_utils.remove_directory(str(self.__environment_path))


    def __str__(self):
        if self.__environment.exists():
            return self.__environment.absolute()
        raise FileNotFoundError(f'Environment {self.__env_name} not found.')


    def __asterix_patch(self, path : pathlib.Path, prefix : str) -> Union[str, None]:
        """Returns the first file path that matches prefix.

        pathlib.Path seems to not support regular expressions in the path name when iterating over directories.
        To counteract this issue, matching the first instance and returning a path for now will be used.

        Args:
            path: Path to folder.
            prefix: Prefix to try and attempt to match.

        Returns:
            Name to first matched instance, else None.
        """
        found_path = None
        if path.exists():
            for subpath in path.iterdir():
                if subpath.name.startswith(prefix) and subpath.is_dir():
                    found_path = subpath.name
                    break
        return found_path


    def _find_interpreter(self) -> pathlib.Path:
        """Finds the Python interepter which is later used to access various executables and scripts inside the environment.

        This function would be typically called when the Python interpreter changes locations, such as one would see when a new virtual environment is stood up.
        For the redundancy of searching for new paths, the function has been protected to avoid general outside use without better reason, potentially moving the interpreter?

        Returns:
            Path reference to interpreter.
        """
        if pathlib.Path(sys.executable) == self.__interpreter:
            if os_utils.get_os() == os_utils.SupportedOS.WINDOWS:
                known_location = pathlib.Path(self.__environment_path, 'python.exe')
                if known_location.exists():
                    self.__interpreter = known_location
                else:
                    # Find the first occurrence of an interpreter - Windows only
                    for path in self.__environment_path.rglob('*'):
                        if path.is_file() and os.access(path, os.X_OK):
                            if path.with_suffix('').name == 'python' and path.suffix == '.exe':
                                self.__interpreter = path
                                break
            elif os_utils.get_os() in [os_utils.SupportedOS.LINUX, os_utils.SupportedOS.MAC]:
                known_location = pathlib.Path(self.__environment_path, 'bin', 'python')
                if known_location.exists():
                    self.__interpreter = known_location
                else:
                    raise OSError(f'Python interpreter doesn\'t exist at known location {known_location.absolute()} on Linux OS.')
        return self.__interpreter


    def cleanup(self):
        """Cleans the virtual environment if created else ignored.

        Shutil.rmtree deletes the directory, Windows this is a bit trickier and if any partition of the
        environment is currently accessed by other processes then rmtree will fail.
        """
        if self.__environment_path.exists():
            os_utils.remove_directory(str(self.__environment_path))


    def dependency_exists(self, package) -> Tuple[str, str]:
        """Checks if a dependency exists.

        Args:
            package: Package to check if it exists.

        Returns:
            Tuple of (package name, version) when the package exists else None.
        """
        pkg_info = (None, None)
        output = pip.list(self, log_output=False)
        for line in output:
            installed_package = line.rstrip().split(' ')
            if package == installed_package[0]:
                pkg_info = (installed_package[0], installed_package[-1])
        return pkg_info


    def executables(self) -> List[pathlib.Path]:
        """Returns the listing of the environments executables (Scripts: Windows, bin: Linux)

        Returns:
            List of files inside the executable directory.
        """
        if os_utils.get_os() == os_utils.SupportedOS.WINDOWS:
            return [x for x in os_utils.retrieve_directory_listing(self.__environment_path, 'Scripts') if x.is_file()]
        elif os_utils.get_os() in [os_utils.SupportedOS.LINUX, os_utils.SupportedOS.MAC]:
            return [x for x in os_utils.retrieve_directory_listing(self.__environment_path, 'bin') if x.is_file()]
        else:
            raise os_utils.PyBuildOSError()


    def info(self) -> Tuple[tuple, int]:
        """Reports environment information.

        Some build scripts may want to know the information of the environment being used,
        often this may be if the system requires a specific Python to launch the build script with.

        Returns:
            Tuple of (sys.version_info, Python Bit)
        """
        return (tuple(sys.version_info), struct.calcsize('P') * 8)


    def libs(self) -> List[pathlib.Path]:
        """Returns the listing of the environments executables (Libs: Windows, lib64, lib: Linux)

        Returns:
            List of files inside the library directory.
        """
        if os_utils.get_os() == os_utils.SupportedOS.WINDOWS:
            return os_utils.retrieve_directory_listing(self.__environment_path, 'Libs')
        elif os_utils.get_os() in [os_utils.SupportedOS.LINUX, os_utils.SupportedOS.MAC]:
            return os_utils.retrieve_directory_listing(self.__environment_path, 'lib', self.__asterix_patch(pathlib.Path(self.__environment_path, 'lib'), 'python'))
        else:
            raise os_utils.PyBuildOSError()


    def name(self) -> str:
        """Returns name of environment.
        """
        return self.__env_name


    def retrieve(self, file : str) -> List[pathlib.Path]:
        """Returns the file listing.

        Returns:
            List of files and directories inside the specified `file`.
        """
        if file in self.__environment_dict:
            return self.__environment_dict


    def python(self) -> pathlib.Path:
        """Grabs the Python interpreter located inside the environment.
        Returns:
            The known location of the Python interpreter, by default sys.executable but may be changed later.
        """
        return self.__interpreter


    def wipe(self) -> bool:
        """Wipes the entirety of the workspace of all installations.

        A developer may want the workspace they either created or are currently running in wiped prior to installing
        additional dependencies, etc. This function is only to be used by experienced users and should be avoided if possible.

        Returns:
            True if the environment was wiped successfully.

        Raises:
            OSError if the environment is unable to be wiped. The process runs through pip
        """
        successful = False
        # Open a temporaryfile
        with NamedTemporaryFile(delete=False) as tmpfd:
            tmpfd.close()
            requirements_txt = pathlib.Path(tmpfd.name)
            pip.freeze(self, tmpfd.name)
            if requirements_txt.exists():
                if file_utils.process_requirements(requirements_txt):
                    pip.uninstall(self, None, requirement=tmpfd.name)
                successful = True
            os_utils.remove_file(requirements_txt)
        return successful