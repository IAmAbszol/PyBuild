""""Operating System utilities for PyBuild.

    This class acts as a utilities class which provides helpful OS related information.

"""
import logging
import pathlib
import platform
import shutil

from enum import Enum
from typing import List, Match


class PyBuildOSError(Exception):
    def __init__(self):
        super(PyBuildOSError, self).__init__(f'OS {get_os()} not supported by PyBuild.')


class SupportedOS(Enum):
    WINDOWS = 0
    LINUX = 1
    MAC = 2


def get_os() -> SupportedOS:
    """Retreive OS specifics.

    Returns:
        Enum class, SupportedOS.
    """
    operating_system = platform.system().lower()
    if operating_system == 'windows':
        return SupportedOS.WINDOWS
    elif operating_system == 'linux':
        return SupportedOS.LINUX
    elif operating_system == 'darwin':
        return SupportedOS.MAC
    else:
        raise OSError(f'Operating System {operating_system} not supported by PyBuild.')


def remove_directory(dir_name : pathlib.Path, force=True):
    """Removes the directory specified by dir_name.

    Args:
        dir_name: Name of directory to be removed.
        force: Force directory removal (Linux Only).
    """
    # TODO: rmtree has onerror which takes a call back.
    #       If the error may be traced as to which folder, permission changes and other attempts
    #       to bypass Windows silliness (.git locks on folders), removing processes from process, etc.
    try:
        shutil.rmtree(dir_name)
    except FileNotFoundError as fnfe:
        logging.error(fnfe)


def remove_file(file_name : pathlib.Path):
    """Removes the file specified by file_name.

    Args:
        file_name: Name of file to remove.
    """
    file_name.unlink()


def retrieve_directory_listing(environment : pathlib.Path, *target : str) -> List[pathlib.Path]:
    """Retreives the directory listing given the environment name provided.

    Args:
        env_name: Environment class.
        target: Single or multiple strings provided that extend from base path.

    Returns:
        List of paths from the directory listing.
    """
    if any(['..' in x for x in target]):
        raise ValueError('Backing out from directories not supported.')
    if environment.exists():
        path = pathlib.Path(environment, *target)
        if path.exists():
            return [x for x in path.iterdir()]
        raise FileNotFoundError(f'File path {path} not found.')
    raise FileNotFoundError(f'Environment {environment} not found.')
