from setuptools import setup, find_packages

__version__ = "0.2.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'pybuildme',
    python_requires='>=3.7',
    packages = find_packages(),
    install_requires=[],
    version = __version__,
    description = 'PyBuild is a build environment for Python that starts from the virtual environment upwards, must be installed on base system prior to running.',
    # long_description = long_description,
    author = 'Kyle Darling',
    author_email = 'kdarling95@yahoo.com',
    url = 'https://github.com/IAmAbszol/PyBuild',
    download_url = '',
    keywords = ['build', 'python', 'automation', 'git', 'framework'],
    classifiers = [],
    license = "MIT",
    include_package_data=True
)
