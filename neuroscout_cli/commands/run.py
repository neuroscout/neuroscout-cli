from neuroscout_cli.commands.base import Command
from neuroscout_cli.commands.install import Install
from fitlins.cli.run import run_fitlins
from pathlib import Path
import logging
import tarfile
import tempfile

# Options not to be passed onto fitlins
INVALID = ['--unlock', '--neurovault', '--version', '--help', '--install-dir',
           'run', '<bundle_id>', '--dataset-name']


class Run(Command):
    ''' Command for running neuroscout workflows. '''

    def run(self):
        # Download bundle and install dataset if necessary
        install = Install(self.options.copy())
        bundle_path = install.run()
        preproc_path = str(install.preproc_dir.absolute())
        out_dir = Path(self.options.pop('<outdir>')) / install.bundle_id

        fitlins_args = [
            preproc_path,
            str(out_dir),
            'dataset',
            '--model={}'.format((bundle_path / 'model.json').absolute()),
            '--ignore=/(fmriprep.*$(?<=tsv))/',
            '--derivatives={} {}'.format(
                bundle_path, preproc_path),
        ]

        neurovault = self.options.pop('--neurovault', 'enable')
        assert neurovault in ['enable', 'disable', 'force']

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

        if neurovault != 'disable':

            logging.info("Uploading results to NeuroVault...")

            # Find files
            images = out_dir / 'fitlins'

            ses_dirs = [a for a in images.glob('ses*') if a.is_dir()]
            if ses_dirs:  # If session, look for stat files in session folder
                images = images / ses_dirs[0]

            images = images.glob('*stat*.nii.gz')

            # Make tarball
            with tempfile.NamedTemporaryFile() as tf:
                with tarfile.open(fileobj=tf.file, mode="w:gz") as tar:
                    for path in images:
                        tar.add(path.absolute(), arcname=path.parts[-1])

                # Upload results NeuroVault
                self.api.analyses.upload_neurovault(
                    self.bundle_id, tf.name,
                    install.resources['validation_hash'],
                    force=neurovault == 'force')
