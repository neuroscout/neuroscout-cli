# neuroscout-cli ⚜️
![Docker Build Status](https://img.shields.io/docker/cloud/build/neuroscout/neuroscout-cli.svg)

The neuroscout command line interface allows you to easily execute analyses created on neuroscout.org. neuroscout-cli automatically fetches analysis dependencies (including data, and analysis specifications), fits a GLM model to the BIDS dataset, and produces shareable reports of the results.

neuroscout-cli uses [FitLins](https://github.com/poldracklab/fitlins) to estimate linear models using the BIDS model specification.

#### Installation
The easiest way to get Neuroscout running is using Docker. Just pull it from Docker hub!

    docker pull neuroscout/neuroscout-cli
    
You can also pull a pre-built singularity image from Github Packages as well:

    singularity pull oras://ghcr.io/neuroscout/neuroscout-cli:master

#### Quickstart
Assuming you've already created an analysis on neuroscout.org, you can run it in one line using the analysis_id (e.g.: `5xH93`):

    docker run -it -v /local/outdir:/outdir neuroscout/neuroscout-cli run 5xH93 /outdir

Neuroscout will download the necessary images, analysis bundle, fit your model, and upload group images to NeuroVault.

For more information, see the Neuroscout [documentation](https://neuroscout.github.io/neuroscout/cli/).