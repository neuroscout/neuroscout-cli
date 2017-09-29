"""
neuroscout

Usage:
    neuroscout run [options] <bundle_file>
    neuroscout -h | --help
    neuroscout --version

Options:
    -h --help           Show this screen.
    --version           Show version.

Examples:
    neuroscout run ns_bundle.json

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
    import neuroscout_cli.workflows as wfs
    args = docopt(__doc__, version=VERSION)
    print args
