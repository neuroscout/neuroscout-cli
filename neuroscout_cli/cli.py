"""
neuroscout

Usage:
    neuroscout run [-nu] [options] <outdir> <bundle_id>...
    neuroscout install [-nu --install_dir=<dir>] <bundle_id>...
    neuroscout ls <bundle_id>
    neuroscout -h | --help
    neuroscout --version

Options:
    --install_dir=<dir>     Directory to download dataset and bundle [default: .]
    --work-dir=<dir>        Working directory
    --n-cpus=<n>            Maximum number of threads across all processes [default: 1]
    --dataset-name=<name>   Manually specify dataset name
    -n --no-download        Dont download dataset
    -u --unlock             Unlock datalad dataset

Commands:
    run                     Runs a first level, group level, or full analysis.
    install                 Installs a bundle and/or dataset.
    ls                      Lists the available files in a bundle's dataset.

Examples:
    neuroscout run -n 5xhaS /out
    neuroscout run 5xhaS 38fdx /out

Help:
    For help using this tool, please open an issue on the Github
    repository: https://github.com/neuroscout/neuroscout-cli.

    For help using neuroscout and creating a bundle, visit www.neuroscout.org.
"""

from docopt import docopt
from . import __version__ as VERSION
import sys
from copy import deepcopy

def main():
    # CLI entry point
    import neuroscout_cli.commands
    args = docopt(__doc__, version=VERSION)

    for (k, v) in args.items():
        if hasattr(neuroscout_cli.commands, k) and v:
            k = k[0].upper() + k[1:]
            command = getattr(neuroscout_cli.commands, k)
            if k in ['Run', 'Install']:
                bundles = args.pop('<bundle_id>')
                # Loop over bundles
                for b in bundles:
                    print("Running bundle {}".format(b))
                    args['<bundle_id>'] = b
                    command(deepcopy(args)).run()
            sys.exit(0)
