"""Manages documentation creation.

    Developers may want to add documentation during the build stage of their software, this can help.

    Basic Usage:

    ```
    from pybuild import pdoc
    pdoc.make('pybuild', out='doc', html=True, overwrite=True)
    ```

"""
import inspect
import logging

from pathlib import Path
from typing import List, Tuple, Union

from pybuild import pip
from pybuild.environment import Environment
from pybuild.utils import process_utils


def make(environment : Environment, 
         package : str,
         config : str=None, 
         filter : str=None,
         force : bool=False,
         html : bool=True,
         pdf : bool=False,
         output_dir : str='.',
         template_dir : str=None,
         close_stdin : str=None,
         http : Union[str,int]=None,
         skip_errors : bool=False,
         **kwargs) -> Path:
    """Creates documentation using Pdoc.

    Pdoc allows the developer to generate documentation during the build stage.
    Additional options have been provided by Pdoc that supports custom templates, etc.

    Returns:
        Path to generated documentation.

    Raises:
        ValueError: When Pdoc wasn't able to create the documentation.
        FileNotFoundError: 
    """
    arg_spec = inspect.getfullargspec(make)
    args = arg_spec.args[len(arg_spec.args) - len(arg_spec.defaults):]
    command_string = []
    for arg in args:
        processed_arg = arg.replace('_', '-')
        if str(eval(arg)) == 'True':
            command_string.append('--{}'.format(processed_arg))
        elif str(eval(arg)) not in ['False', 'None']:
            command_string.append('--{} {}'.format(processed_arg, eval(arg)))

    pip.install(environment, 'pdoc3', **kwargs)
    rc = process_utils.create_process(str(environment.python()), '-m pdoc {} {}'.format(' '.join(command_string), package))
    if rc != 0:
        raise ValueError('Failed to create documenation.')
    logging.info(f'Successfully made Pdoc documentation.')
    out_path = Path(Path.cwd(), output_dir, Path(package).name)
    if not out_path.exists():
        raise FileNotFoundError('Pdoc documentation failed to write to designated location.')
    return out_path