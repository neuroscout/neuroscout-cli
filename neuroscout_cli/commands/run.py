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

        ## Set up fitlins args
        fitlins_args = [
            install_command.dataset_dir.as_posix(),
            self.options.pop('o', '.'),
            'dataset',
            '--model={}'.format((bundle_path / 'model.json').as_posix())
        ]

        # Add remaining optional arguments
        for name, value in self.options.items():
            if name.startswith('-'):
                fitlins_args.append('{} {}'.format(name, value))

        print(fitlins_args)

        # Call fitlins as if CLI
        runfitlns(fitlins_args)
