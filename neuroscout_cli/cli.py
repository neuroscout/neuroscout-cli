"""
neuroscout

Usage:
    neuroscout run <bundle_id> [-a <analysis_level>] [-i <install_dir> ] [-w <work_dir>] [-o <out_dir>] [--nthreads=<n>] [--debug]
    neuroscout install <bundle_id> [bundle|data] [-i <install_dir>] [--debug]
    neuroscout ls <bundle_id>
    neuroscout -h | --help
    neuroscout --version

Options:
    -a <analysis_level>     Processing stage to be run (default: dataset)
    -i <install_dir>        Directory to download data and remote files.
    -o <out_dir>            Output directory.
    -w <work_dir>           Working directory.
    --nthreads=<n>          Number of parallel jobs [default: 1].
    -h --help               Show this screen.
    --version               Show version.
    --debug                 Debug level logging

Commands:
    run                     Runs a first level, group level, or full analysis.
    install                 Installs a bundle and/or dataset.
    ls
                        Lists the available files in a bundle's dataset.

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
