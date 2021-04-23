"""
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
    -m, --drop-missing       If contrast is missing in a run, skip.
    -d, --no-datalad-drop    Don't drop DataLad sourcedata. True by default
                             if install-dir is specified.
    -v, --verbose	         Verbose mode
    

Commands:
    run                      Runs analysis.
    install                  Installs a bundle and/or dataset.
    upload                   Upload existing analysis results to Neurovault.
    ls                       Lists the available files in a bundle's dataset.

Examples:
    neuroscout run 5xhaS /out --n-cpus=10
    neuroscout run 5xhaS 38fdx /out

Help:
    For help using this tool, please open an issue on the Github
    repository: https://github.com/neuroscout/neuroscout-cli.

    For help using neuroscout and creating a bundle, visit www.neuroscout.org.
"""
import sys
from copy import deepcopy
from docopt import docopt
from neuroscout_cli import __version__ as VERSION
import neuroscout_cli.commands as ncl
import logging
logging.getLogger().setLevel(logging.INFO)


def main():
    # CLI entry point
    args = docopt(__doc__, version=VERSION)

    for (k, val) in args.items():
        if hasattr(ncl, k) and val:
            k = k[0].upper() + k[1:]
            command = getattr(ncl, k)
            if k in ['Run', 'Install', 'Upload']:
                bundles = args.pop('<bundle_id>')
                # Loop over bundles
                for bundle in bundles:
                    logging.info("Analysis ID : {}".format(bundle))
                    args['<bundle_id>'] = bundle
                    command(deepcopy(args)).run()
            sys.exit(0)
