from neuroscout_cli.commands.base import Command
from neuroscout_cli.commands.install import Install
from fitlins.cli.run import run_fitlins
from pathlib import Path

# Options not to be passed onto fitlins
INVALID = ['--unlock', '--no-download', '--version', '--help', '--install-dir',
           'run', '<bundle_id>', '--dataset-name']


class Run(Command):
    ''' Command for running neuroscout workflows. '''

    def run(self):
        # Download bundle and install dataset if necessary
        install = Install(self.options.copy())
        bundle_path = install.run()

        out_dir = Path(self.options.pop('<outdir>')) / install.bundle_id

        dataset_dir = install.dataset_dir.absolute()

        fitlins_args = [
            str(dataset_dir),
            str(out_dir),
            'dataset',
            '--model={}'.format((bundle_path / 'model.json').absolute()),
            '--exclude=(fmriprep.*$(?<=tsv))'.format(bundle_path.parts[-1]),
            '--derivatives={} {}'.format(
                bundle_path, install.preproc_dir.absolute() / 'fmriprep'),
        ]

        # Fitlins invalid keys
        for k in INVALID:
            self.options.pop(k, None)

        # Add remaining optional arguments
        for name, value in self.options.items():
            if name.startswith('--'):
                if value is True:
                    fitlins_args.append('{}'.format(name))
                if value is not None and value is not False:
                    fitlins_args.append('{}={}'.format(name, value))
            else:
                if value is not False and value is not None:
                    fitlins_args.append('{} {}'.format(name, value))

        # Call fitlins as if CLI
        run_fitlins(fitlins_args)
