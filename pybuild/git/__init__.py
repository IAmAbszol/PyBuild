"""Handles git related operations inside PyBuild.

    PyBuild allows for packages and modules not hosted on PyPi to be pulled from their respective repositories. This
    module in particular will allow for clone functionality provided by git, git will of course need
    to be installed on the system as binaries will not be stored for it to use.

    Basic Usage:

    ```
    from pybuild import git

    git.clone('https://github.com/foobar/baz.git', branch='dev', progress=True)
    ```

"""
import logging

from pathlib import Path

from pybuild.utils import file_utils, process_utils


def clone(url, destination : str=None, branch : str=None, progress : bool=True) -> Path:
    """Clones the given URL using git.

    Clone allows the developer to download additional modules to their designated locations.

    Args:
        url: URL to access git repository.
        destination: Location to store cloned repository, default is current working directory.
        branch: Branch to checkout when cloning, leave None for default.
        progress: Display progress bar while cloning repository.

    Returns:
        Path to cloned repository, destination will be this return value.
        None if the function fails to find validate the repository successfully.
        
    Raises:
        ValueError: Raised when process fails to execute properly.
        FileNotFoundError: Raised when git clone successfully runs but the destination cannot be found.

    """
    if file_utils.validate_url(url):
        url_path = Path(url)
        destination = destination if destination else url_path.with_suffix('').name
        git_command = f'clone {url} {destination}'
        git_command += f' -b {branch}' if branch else ''
        git_command += ' --progress' if progress else ''
        rc = process_utils.create_process('git', git_command)
        if rc != 0:
            raise ValueError('Failed to clone repository.')
        cloned_path = Path(Path.cwd(), destination)
        if not cloned_path.exists():
            raise FileNotFoundError(f'Failed to find {destination}.')
        return cloned_path
    else:
        logging.error('Invalid URL detected.')
