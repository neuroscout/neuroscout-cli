# neuroscout-cli ⚜️
![Docker Build Status](https://img.shields.io/docker/cloud/build/neuroscout/neuroscout-cli.svg)

The neuroscout command line interface allows you to easily execute analyses created on neuroscout.org. neuroscout-cli automatically fetches analysis dependencies (including data, and analysis specifications), fits a GLM model to the BIDS dataset, and produces shareable reports of the results.

neuroscout-cli uses [FitLins](https://github.com/poldracklab/fitlins) to estimate linear models using the BIDS model specification.

#### Installation
The easiest way to get Neuroscout running is using Docker. Just pull it from Docker hub!

    docker pull neuroscout/neuroscout-cli
    
You can also pull a pre-built singularity image from Github Packages as well:


    singularity pull oras://ghcr.io/neuroscout/neuroscout-cli:master

#### Usage
Neuroscout is easy to use. Assuming you've already created an analysis on neuroscout.org, and have its analysis id (e.g.: `5xH93`) you can run it in one line:

    docker run -it neuroscout/neuroscout-cli run /outdir 5xH93

Neuroscout will download the necessary images, analysis bundle, fit your model, and upload group images to NeuroVault.

To cache the downloaded data, and output the results to your local filesystem, mount the appropriate volumes:

    docker run -it -v /local/datadir:/data -v /local/outdir:/out neuroscout/neuroscout-cli run /out 5xH93 -i /data

This will create an output folder for your analysis (e.g. `neuroscout-5xH93`), which contains the fitted statistical maps, as well as the input event files from Neuroscout.

In addition, the input fMRI images will be saved in `/local/datadir/{dataset_name}` as a DataLad dataset. Next time you fit a model from the same dataset,
you won't have to re-download the images that you used for this analysis. 

See the output of `neuroscout --help` for more information:

```
neuroscout

Usage:
    neuroscout run [-mfuvd -i <dir> -w <dir> -s <k> -c <n> -n <nv> -e <es>] <outdir> <bundle_id>...
    neuroscout install [-ui <dir>] <outdir> <bundle_id>...
    neuroscout upload [-f -n <nv>] <outdir> <bundle_id>...
    neuroscout ls <bundle_id>
    neuroscout -h | --help
    neuroscout --version

Options:
    -i, --install-dir <dir>  Optional directory to cache input images
    -w, --work-dir <dir>     Optional Fitlins working directory 
    -c, --n-cpus <n>         Maximum number of threads across all processes
                             [default: 1]
    -s, --smoothing <k>      Smoothing kernel FWHM at group level
                             [default: 4]
    -u, --unlock             Unlock datalad dataset
    -n, --neurovault <nv>    Upload mode (disable, all, or group)
                             [default: group]
    -e, --estimator <es>     Estimator to use for first-level model
                             [default: nistats]
    -f, --force-neurovault   Force upload, if a NV collection already exists
    -m, --skip-missing       If contrast is missing in a run, skip run.
    -d, --no-drop            Don't drop DataLad inputs. Also true, if
                             an install-dir is specified.
    -v, --verbose	         Verbose mode

Commands:
    run                      Runs analysis.
    install                  Installs a bundle and/or dataset.
    ls                       Lists the available files in a bundle's dataset.
```
