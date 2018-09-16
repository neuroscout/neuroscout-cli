# neuroscout-cli ⚜️
![Docker Build Status](https://img.shields.io/docker/build/neuroscout/neuroscout-cli.svg)


The neuroscout command line interface allows you to easily execute analyses created on neuroscout.org. neuroscout-cli automatically fetches analysis dependencies (including data, and analysis specifications), fits a GLM model to the BIDS dataset, and produces shareable reports of the results.

neuroscout-cli uses [FitLins](https://github.com/poldracklab/fitlins) to estimate linear models using the BIDS model specification.

#### Installation
The easiest way to get Neuroscout running is using Docker. Just pull it from Docker hub!

    docker pull neuroscout/neuroscout-cli

#### Usage
Neuroscout is easy to use. Assuming you've already created an analysis on neuroscout.org, and have its analysis id (e.g.: `5xH937f`) you can run it in one line:

    docker run -it neuroscout/neuroscout-cli run /outdir 5xH937f

Neuroscout will download the necessary images, analysis bundle, and fit your model.

To cache the downloaded data, and output the results to a separate folder, mount the appropriate volumes:

    docker run -it -v /local/datadir:/data -v /local/outdir:/out neuroscout/neuroscout-cli run /out 5xH937f

See the output of `neuroscout --help` for more information:

```
Usage:
    neuroscout run [-nui <dir> -c <n> -w <dir> -d <n>] <outdir> <bundle_id>...
    neuroscout install [-nui <dir>] <bundle_id>...
    neuroscout ls <bundle_id>
    neuroscout -h | --help
    neuroscout --version

Options:
    -i, --install-dir <dir>  Directory to download data [default: .]
    -w, --work-dir <dir>     Working directory
    -c, --n-cpus <n>         Maximum number of threads across all processes [default: 1]
    -d, --dataset-name <n>   Manually specify dataset name
    -n, --no-download        Dont download dataset
    -u, --unlock             Unlock datalad dataset

Commands:
    run                      Runs a first level, group level, or full analysis.
    install                  Installs a bundle and/or dataset.
    ls                       Lists the available files in a bundle's dataset.
```
