# PyBuild
## Developed by Kyle Darling

---

### Purpose
PyBuild was developed to aid in quick, robust, procedurally generated build environments where the user can develop scripts quick in setting up their Python environment to their needs. The difference between PyBuild and other build frameworks available in Python is that PyBuild focuses on outside packages that may not be available to pip install or build itself into an executable.

PyBuild relies heavily on the **Environment** class where initially it uses the Python interpreter used to run a PyBuild script as it's main environment, later this can change with the use of **VirtualEnv** where a virtual environment can be used instead, effectively swapping the environment to the virtual environment.

### Basic Usage
PyBuild supports quick and easy installations of packages.
```
from pybuild import pip
from pybuild.environment import Environment

environment = Environment('pybuild_demo')
pip.install(environment, 'matplotlib>=1.0.0', 'numpy', 'virtualenv==16.6.0')
```
> *pybuild_demo* would become the name of the virtual environment.

Developers may also use the **with** context in Python to use an environment. 
```
from pybuild import pip
from pybuild.environment import environment
from pybuild.virtualenv import VirtualEnv

with Environment('pybuild_demo') as environment:
    Virtualenv(environment)
    pip.install(environment, 'matplotlib')
```
>*Virtual environments are deleted after completion.*

The pip package inside PyBuild acts as a wrapper like most things do in PyBuild around the Python interpreter, accessing scripts as needed. This means that PyBuild supports additional arguments for installations and uninstallations.

```
from pybuild import pip
from pybuild.environment import Environment

with Environment('pybuild_demo') as environment:
    pip.install(environment, 'matplotlib', no_cache_dir=True)
```
>no_cache_dir will be parsed and used as an argument to pip install.

### Demonstration
Now that you understand how PyBuild works by using the *Environment* class and the general functionality of PyBuild has been demonstrated, how about a more advanced setup?

### To Do
PyBuild is rather new project that always has module integration in mind when developing and with that there exists additional modules that should be added.

- Common modules class for any class objects created to help guide users.
- Registering external modules to PyBuild, dynamic module loading would be required.
- Add more modules! The suite right now has been trimmed down to personal usage of the modules but other virtual environments, documentation, etc are always welcomed.
- Add master demo.