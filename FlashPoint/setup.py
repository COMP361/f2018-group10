from setuptools import setup, find_packages

"""This script defines the setup for our package. It contains basic information and dependencies.
It is called when we install our package, and creates an executable for the game."""

setup(
    name='FlashPoint',
    version='1.0.0',
    packages=find_packages(exclude=["*.tests"]),  # This must match the directory (package) containing our code.
    install_requires=[  # All dependencies must be in this list!!!
        'pygame'
    ],
    entry_points="""
        [console_scripts]
        FlashPoint=src.main:run
    """  # Running "FlashPoint" from the command line will now start the program.
)
