"""
neuroscout-cli

Usage:
    neuroscout run [options] <outdir> <bundle_id> [<fitlins_args>...]
    neuroscout install [--install-dir <dir>] <outdir> <bundle_id>
    neuroscout upload [--force-upload --neurovault <nv>] <outdir> <bundle_id>
    neuroscout -h | --help
    neuroscout --version

Options:
    --install-dir <dir>  Optional directory to cache input datasets
    --neurovault <nv>    Upload mode (disable, all, or group)
                         [default: group]
    --force-upload       Force upload, if a NV collection already exists
    
Commands:
    run                      Runs analysis using FitLins. Installs inputs & uploads results automatically. 
                             You can pass arbitrary arguments to FitLins after the <bundle_id>.
    install                  Installs a bundle and/or dataset without executing analysis.
    upload                   Upload existing analysis results to Neurovault.

Example:
    neuroscout run --force-upload 5xhaS /out --n-cpus=10

Help:
    For help using neuroscout, visit https://neuroscout.github.io/neuroscout/cli/
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
            bundle = args['<bundle_id>']
            print(args)
            # Loop over bundles
            logging.info("Analysis ID : {}".format(bundle))
            retcode = command(deepcopy(args)).run()
            
            # If any execution fails, then exit
            if retcode != 0:
                sys.exit(retcode)
            sys.exit(0)
