from setuptools import setup, find_packages
from neuroscout_cli import  __version__
PACKAGES = find_packages()

setup(
    name='neuroscout-cli',
    version=__version__,
    description='Neuroscout command line interface and neuroimaging workflows.',
    url='https://github.com/PsychoinformaticsLab/neuroscout-cli',
    author='UT Psychoinformatics Lab',
    author_email='delavega@utexas.edu',
    license='MIT',
    packages=PACKAGES,
    keywords='cli',
    entry_points={
        'console_scripts': [
            'neuroscout=neuroscout_cli.cli:main'
        ]
    }
)
