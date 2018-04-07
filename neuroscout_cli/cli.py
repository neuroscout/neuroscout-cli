"""
neuroscout

Usage:
    neuroscout run <bundle_id> [-dn -w <work_dir> -o <out_dir> -i <install_dir> --nthreads=<n>]
    neuroscout install <bundle_id> [-dn -i <install_dir>]
    neuroscout ls <bundle_id>
    neuroscout -h | --help
    neuroscout --version

Options:
    -i <install_dir>        Directory to download dataset and bundle [default: .]
    -o <out_dir>            Output directory
    -w <work_dir>           Working directory
    --nthreads=<n>          Number of parallel jobs [default: 1]
    -n, --no-download       Dont download dataset (if available locally)
    -h --help               Show this screen
    -v, --version           Show version
    -d, --debug             Debug mode

Commands:
    run                     Runs a first level, group level, or full analysis.
    install                 Installs a bundle and/or dataset.
    ls                      Lists the available files in a bundle's dataset.

Examples:
    neuroscout run dataset bundle.json .

Help:
    For help using this tool, please open an issue on the Github
    repository: https://github.com/PsychoinformaticsLab/neuroscout-cli.

    For help using neuroscout and creating a bundle, visit www.neuroscout.org.
"""

from docopt import docopt
from . import __version__ as VERSION
import logging
import sys

def main():
    # CLI entry point
    import neuroscout_cli.commands
    args = docopt(__doc__, version=VERSION)

    if args.get('--debug'):
        logging.basicConfig(level=logging.DEBUG)

    for (k, v) in args.items():
        if hasattr(neuroscout_cli.commands, k) and v:
            k = k[0].upper() + k[1:]
            command = getattr(neuroscout_cli.commands, k)
            command = command(args)
            command.run()
            sys.exit(0)
