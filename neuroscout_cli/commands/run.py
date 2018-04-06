from neuroscout_cli.commands.base import Command
from neuroscout_cli.commands.install import Install
from fitlins.cli.run import run as runfitlns

class Run(Command):

    ''' Command for running neuroscout workflows. '''

    def run(self):
        if self.options.pop('--no-install', False):
            self.options['bundle'] = True

        install_command = Install(self.options.copy())
        bundle_path, bids_dir = install_command.run()

        all_args = [
            bids_dir,
            self.options.pop('o', '.'),
            self.options.pop('-a', 'dataset'),
            '--model={}'.format((bundle_path / 'model.json').as_posix())
        ]

        # Add remaining optional arguments

        for name, value in self.options.items():
            if name.startswith('-'):
                all_args.append('{} {}'.format(name, value))

        # Call fitlins as if CLI
        runfitlns(all_args)
