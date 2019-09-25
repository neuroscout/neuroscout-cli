"""
neuroscout

Usage:
    neuroscout run [-ui <dir> -s <k> -w <dir> -c <n> -n <nv> -d] <outdir> <bundle_id>...
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
    -n, --neurovault <nv>    Upload mode (disable, force, or enable)
                             [default: enable]
    -d, --drop-missing       Drop missing contrast

Commands:
    run                      Runs a first level, group level, or full analysis.
    install                  Installs a bundle and/or dataset.
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
            if k in ['Run', 'Install']:
                bundles = args.pop('<bundle_id>')
                # Loop over bundles
                for bundle in bundles:
                    logging.info("Running analysis : {}".format(bundle))
                    args['<bundle_id>'] = bundle
                    command(deepcopy(args)).run()
            sys.exit(0)
