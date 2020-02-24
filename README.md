# neuroscout-cli ⚜️
![Docker Build Status](https://img.shields.io/docker/cloud/build/neuroscout/neuroscout-cli.svg)

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
neuroscout

Usage:
    neuroscout run [-dfu -i <dir> -s <k> -w <dir> -c <n> -n <nv>] <outdir> <bundle_id>...
    neuroscout install [-ui <dir>] <bundle_id>...
    neuroscout ls <bundle_id>
    neuroscout -h | --help
    neuroscout --version

Options:
    -i, --install-dir <dir>  Directory to download data [default: .]
    -w, --work-dir <dir>     Working directory
    -c, --n-cpus <n>         Maximum number of threads across all processes
                             [default: 1]
    -s, --smoothing <k>      Smoothing kernel FWHM at group level
                             [default: 4]
    -u, --unlock             Unlock datalad dataset
    -n, --neurovault <nv>    Upload mode (disable, all, or group)
                             [default: group]
    -f, --force-neurovault   Force upload, if a NV collection already exists
    -d, --drop-missing       Drop missing contrast

Commands:
    run                      Runs analysis.
    install                  Installs a bundle and/or dataset.
    ls                       Lists the available files in a bundle's dataset.
```
