"""File system utilities for PyBuild.

    This class provides a general interface for various file related operations that a user may experience while using PyBuild.

"""
import re
import shutil

from pathlib import Path
from tempfile import NamedTemporaryFile

from pybuild.utils import os_utils


def copy(src, dst, *args):
    """Copy files and directories in PyBuild.
    
    Some builds require the copying and movement of files around the system.
    """
    return shutil.copy2(src, dst, args)


def move(src, dst):
    """Move files and directories in PyBuild.
    
    Some builds require the moving of files around the system.
    """
    return shutil.move(src, dst)


def process_requirements(requirements : Path) -> bool:
    """Processes a requirements.txt or any named variant that came off of pip.freeze.

    Certain environments have packages installed as editable which cause uninstallation related issues
    when wiping the environment using Environment.wipe. To circumvent this, processing the requirements.txt or
    any named variant that removes the editable comment and following line will fix this issue.

    Returns:
        True if the process completed successfully else False.

    Raises:
        FileNotFoundError: When requirements wasn't able to be found.
        Additional errors raised by shutil.
    """
    if requirements.exists():
        with open(requirements, 'r') as fd:
            with NamedTemporaryFile(delete=False) as tmpfd:
                index, lines = 0, fd.readlines()
                while index < len(lines):
                    line = lines[index]
                    if not '# Editable install' in line:
                        tmpfd.write(bytes(line, encoding='utf-8'))
                    else:
                        index += 1
                    index += 1
                tmpfd.flush()
                shutil.copyfile(tmpfd.name, requirements)
                tmpfd.close()
                os_utils.remove_file(Path(tmpfd.name))
                return True
    else:
        raise FileNotFoundError(f'Unable to find requirements, path provided {str(requirements)}.')


def touch(dst):
    """Creates a file.

    Creates a file on Windows, Linux or Mac dependening on the file provided in dst.s
    
    Args:
        dst: File to create.s
    """
    with open(dst, 'w') as tmp:
        pass


def validate_url(url):
    
    # URL regex validation from Django
    # https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
    url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_regex, url) is not None