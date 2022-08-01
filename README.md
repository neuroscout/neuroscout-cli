# neuroscout-cli ⚜️

[![Documentation Status](https://readthedocs.org/projects/neuroscout-cli/badge/?version=latest)](https://neuroscout-cli.readthedocs.io/en/latest/?badge=latest) [![PyPI version](https://badge.fury.io/py/neuroscout-cli.svg)](https://badge.fury.io/py/neuroscout-cli) ![Docker Build Status](https://img.shields.io/docker/cloud/build/neuroscout/neuroscout-cli.svg)

The neuroscout command line interface allows you to easily execute analyses created on neuroscout.org. neuroscout-cli automatically fetches analysis dependencies (including data, and analysis specifications), fits a GLM model to the BIDS dataset, and produces shareable reports of the results.

neuroscout-cli uses [FitLins](https://github.com/poldracklab/fitlins) to estimate linear models using the BIDS model specification.

## Learn more

For more information, visit the official [Neuroscout Docs](https://neuroscout.org/docs) and the [Neuroscout CLI Reference](https://neuroscout-cli.readthedocs.io/en/latest).