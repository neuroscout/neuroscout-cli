"""
neuroscout

Usage:
    neuroscout run first_level [-b <local_bids_dir>|-i <install_dir>|-w <work_dir>|-c|--jobs=<n>|--disable-datalad] <bundle> <out_dir>
    neuroscout make first_level [-b <local_bids_dir>|-i <install_dir>|-w <work_dir>|-c|--jobs=<n>|--disable-datalad] <bundle> [<out_dir>]
    neuroscout run group [-w <work_dir>|-c|--jobs=<n>] <firstlv_dir> <output>
    neuroscout make group <firstlv_dir> [<output>]
    neuroscout -h | --help
    neuroscout --version

Options:
    -b <local_bids_dir>     Optional local copy of remote directory.
    -i <install_dir>        Path to install dataset with datalad.
    -w <work_dir>           Working directory.
    -c                      Stop on first crash.
    --jobs=<n>              Number of parallel jobs [default: 1].
    --disable-datalad       Don't attempt to use datalad to fetch data.
    -h --help               Show this screen.
    --version               Show version.

Examples:
    neuroscout first run bundle.json .

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
    import neuroscout_cli.workflows.fmri_bids_firstlevel as first_level
    import neuroscout_cli.workflows.fmri_group as group_level
    args = docopt(__doc__, version=VERSION)
    first = args.pop('first')
    group = args.pop('group')
    if first:
        runner = first_level.FirstLevel(args)
        runner.execute()
    elif group:
        args = group_level.validate_arguments(args)
        run = args.pop('run')
        args.pop('make')
        jobs = int(args.pop('--jobs'))
        wf = group_level.group_onesample(**args)

        if run:
            if jobs == 1:
                wf.run()
            else:
                wf.run(plugin='MultiProc', plugin_args={'n_procs': jobs})
        else:
            wf
