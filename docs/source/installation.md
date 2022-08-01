# Installation

The recommended way to install `Neuroscout-CLI` is using containers (i.e. Docker or Singularity) to facilitate dependency managment.

For demonstration, it is possible to run `Neuroscout-CLI` in the cloud (for free!) using Google Colab.

## Containerized Execution

### Docker

https://img.shields.io/docker/pulls/neuroscout/neuroscout-cli.svg

For most systems, we recommend using [Docker](https://www.docker.com/resources/what-container). First, follow the instructions for installing [Docker](https://docs.docker.com/engine/install/) on your system.

Next, follow the {doc}`neuroscout:cli/docker` guide in the Neuroscout Docs.

### Singularity

[Singularity](https://sylabs.io/singularity/) containers are a great solution for High Performance Computing (HPC) environments, where _Docker_ cannot typically be used due to more tightly controlled [user privileges](https://researchcomputing.princeton.edu/support/knowledge-base/singularity).

First, check with your HPC administrator that _Singularity_ is available for use. If so, follow our guide on {doc}`neuroscout:cli/singularity` in the offical [Neuroscout Docs](https://neuroscout.org/docs).

## Google Colab

To try Neuroscout without using any local resources, follow our guide to {doc}`neuroscout:cli/Neuroscout_CLI_Colab_Demo`.

Google Colab allows you to execute Jupyer Notebooks for free, using two CPUs for several hours. This should be sufficient for individual Neuroscout analyses. A small demonstration can be run live in ~15 mins. 

## Manually prepared environment using pip

[![PyPI version](https://badge.fury.io/py/neuroscout_cli.svg)](https://badge.fury.io/py/neuroscout_cli)

```{admonition} Danger
Manually installing _neuroscout-cli_ can be difficult due to complex dependencies in the SciPy stack, or fMRI-specific tooling. 
Proceed only if you know what you're doing.
```
Use pip to install _neuroscout-cli_ from PyPI:

    pip install neuroscout-cli