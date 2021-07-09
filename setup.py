from setuptools import setup, find_packages

setup(
    name = 'PyBuild',
    python_requires='>=3.7',
    packages = ['pybuild'],
    install_requires=[],
    version = '0.1.0',
    description = 'PyBuild is a build environment for Python that starts from the virtual environment upwards, must be installed on base system prior to running.',
    author = 'Kyle Darling',
    author_email = 'kdarling95@yahoo.com',
    url = '',
    download_url = '',
    keywords = ['build', 'python', 'automation', 'git'],
    classifiers = [],
    license = "LGPLv3",
    include_package_data=True
)
