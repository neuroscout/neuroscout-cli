from neuroscout_cli.commands.base import Command
from neuroscout_cli.commands.install import Install
from fitlins.cli.run import run_fitlins
from tempfile import mkdtemp
import shutil
from pathlib import Path
import bids

class Run(Command):

    ''' Command for running neuroscout workflows. '''

    def run(self):
        # Download bundle and install dataset if necessary
        install_command = Install(self.options.copy())
        bundle_path = install_command.run()

        out_dir = self.options.pop('-o')
        if out_dir == "bundle_dir":
            out_dir = (install_command.bundle_dir).absolute()

        tmp_out = mkdtemp()

        dataset_dir = install_command.dataset_dir.absolute()

        ## Set up fitlins args
        fitlins_args = [
            dataset_dir.as_posix(),
            tmp_out,
            'dataset',
            '--model={}'.format((bundle_path / 'model.json').absolute().as_posix()),
            '--exclude=.*neuroscout/(?!{}).*'.format(bundle_path.parts[-1])
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

        bids.config.set_options(loop_preproc=True)
        # Call fitlins as if CLI
        run_fitlins(fitlins_args)
        # Copy to out_dir (doing this because of Windows volume)
        shutil.copytree(Path(tmp_out) / 'fitlins', out_dir / 'fitlins')
