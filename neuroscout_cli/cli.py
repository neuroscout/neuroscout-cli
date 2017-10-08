"""
neuroscout

Usage:
    neuroscout run [first_level|group_level] [-i <install_dir>|-w <work_dir>|-o <out_dir>|-c|--jobs=<n>] <bundle_id>
    neuroscout install [bundle|data] [-i <install_dir>] <bundle_id>
    neuroscout get <bundle_id>
    neuroscout -h | --help
    neuroscout --version

Options:
    -i <install_dir>        Directory to download data and remote files.
    -w <work_dir>           Working directory.
    -o <out_dir>            Output directory.
    -c                      Stop on first crash.
    --jobs=<n>              Number of parallel jobs [default: 1].
    -h --help               Show this screen.
    --version               Show version.

Examples:
    neuroscout run first_level bundle.json .

Help:
    For help using this tool, please open an issue on the Github
    repository: https://github.com/PsychoinformaticsLab/neuroscout-cli.

    For help using neuroscout and creating a bundle, visit the main
    neuroscout Github repository:
    https://github.com/PsychoinformaticsLab/neuroscout.
"""

from docopt import docopt
from . import __version__ as VERSION


def main():
    # CLI entry point
    import neuroscout_cli.commands
    args = docopt(__doc__, version=VERSION)

    for (k, v) in args.items():
        if hasattr(neuroscout_cli.commands, k) and v:
            k = k[0].upper() + k[1:]
            command = getattr(neuroscout_cli.commands, k)
            command = command(args)
            command.run()
