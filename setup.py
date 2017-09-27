from setuptools import setup, find_packages
PACKAGES = find_packages()

setup(name='neuroscout-cli',
      version='0.1',
      description='Neuroscout command line interface and neuroimaging workflows.',
      url='https://github.com/PsychoinformaticsLab/neuroscout-cli',
      author='UT Psychoinformatics Lab',
      author_email='delavega@utexas.edu',
      license='MIT',
      packages=PACKAGES)
