from neuroscout_cli.commands.base import Command
from neuroscout_cli.commands.install import Install
from fitlins.cli.run import run as runfitlns
import json

class Run(Command):

    ''' Command for running neuroscout workflows. '''

    def run(self):
        # Download bundle and install dataset if necessary
        install_command = Install(self.options.copy())
        bundle_path = install_command.run()

        ## Edit neuroscout layout
        layout = {
            "name": "neuroscout",
            "include": [".*{}/.*".format(self.bundle_id)]
        }
        json.dump(layout, (bundle_path.parents[0] / 'layout.json').open('w'))

        out_dir = self.options.pop('-o')
        if out_dir == "bundle_dir":
            out_dir = (install_command.bundle_dir).absolute().as_posix()

        dataset_dir = install_command.dataset_dir.absolute()

        ## Set up fitlins args
        fitlins_args = [
            dataset_dir.as_posix(),
            out_dir,
            'dataset',
            '--model={}'.format((bundle_path / 'model.json').absolute().as_posix()),
            '--preproc-dir={}'.format((dataset_dir / 'derivatives' / 'fmriprep').as_posix())
        ]

        # Fitlins invalid keys
        invalid = ['--no-download', '--version', '--help', '-i']
        for k in invalid:
            self.options.pop(k, None)

        # Add remaining optional arguments
        for name, value in self.options.items():
            if name.startswith('--'):
                if value is True:
                    fitlins_args.append('{}'.format(name))
            elif name.startswith('-'):
                if value is not None:
                    fitlins_args.append('{} {}'.format(name, value))

        print(fitlins_args)
        # Call fitlins as if CLI
        runfitlns(fitlins_args)
