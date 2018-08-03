# neuroscout-cli ⚜️
![Docker Build Status](https://img.shields.io/docker/build/neuroscout/neuroscout-cli.svg)


The neuroscout command line interface allows you to easily execute analyses created on neuroscout.org. neuroscout-cli automatically fetches analysis dependencies (including data, and analysis specifications), fits a GLM model to the BIDS dataset, and produces shareable reports of the results.

neuroscout-cli uses [FitLins](https://github.com/poldracklab/fitlins) to estimate linear models using the BIDS model specification.

#### Installation
The easiest way to get Neuroscout running is using Docker. Just pull it from Docker hub!

    docker pull neuroscout/neuroscout-cli

#### Usage
Neuroscout is easy to use. Assuming you've already created an analysis on neuroscout.org, and have its analysis id (e.g.: `5xH937f`) you can run it in one line:

    docker run -it neuroscout/neuroscout-cli run 5xH937f

Neuroscout will download the necessary images, analysis bundle, and fit your model.

To cache the downloaded data, and output the results to a separate folder, mount the appropriate volumes:

    docker run -it -v /local/datadir:/data -v /local/outdir:/out neuroscout/neuroscout-cli run 5xH937f -o /out

See the output of `neuroscout --help` for more information:

```
Usage:
    neuroscout run <bundle_id> [-dn -w <work_dir> -o <out_dir> -i <install_dir> --n-cpus=<n>]
    neuroscout install <bundle_id> [-dn -i <install_dir>]
    neuroscout ls <bundle_id>
    neuroscout -h | --help
    neuroscout --version

Options:
    -i <install_dir>        Directory to download dataset and bundle [default: .]
    -o <out_dir>            Output directory [default: bundle_dir]
    -w <work_dir>           Working directory
    --n-cpus=<n>            Maximum number of threads across all processes [default: 1]
    -n, --no-download       Dont download dataset (if available locally)
    -h --help               Show this screen
    -v, --version           Show version
    -d, --debug             Debug mode

Commands:
    run                     Runs a first level, group level, or full analysis.
    install                 Installs a bundle and/or dataset.
    ls                      Lists the available files in a bundle's dataset.
```
