from neuroscout_cli.commands.base import Command
from neuroscout_cli import __version__ as VERSION
from neuroscout_cli.commands.install import Install
from fitlins.cli.run import run_fitlins
from pathlib import Path
import logging
import re
import json

# Options not to be passed onto fitlins
INVALID = ['--unlock', '--version', '--help', '--install-dir',
           'run', '<bundle_id>', '--dataset-name']


class Run(Command):
    ''' Command for running neuroscout workflows. '''

    def run(self):
        # Download bundle and install dataset if necessary
        install = Install(self.options.copy())
        bundle_path = install.run()
        preproc_path = str(install.preproc_dir.absolute())
        out_dir = Path(self.options.pop('<outdir>')) / install.bundle_id
        smoothing = self.options.pop('--smoothing')
        model_path = (bundle_path / 'model.json').absolute()

        fitlins_args = [
            preproc_path,
            str(out_dir),
            'dataset',
            f'--model={model_path}'
            '--ignore=/(.*desc-confounds_regressors.tsv)/',
            f'--derivatives={bundle_path}'
            f'--smoothing={smoothing}:Dataset'
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
                    fitlins_args.append(f'{name}')
                elif value is not None and value is not False:
                    fitlins_args.append(f'{name}={value}')
            else:
                if value is not False and value is not None:
                    fitlins_args.append(f'{name} {value}')

        # Call fitlins as if CLI
        retcode = run_fitlins(fitlins_args)

        if retcode == 0:
            if neurovault != 'disable':

                model = json.load(open(model_path, 'r'))
                n_subjects = len(model['Input']['Subject'])

                logging.info("Uploading results to NeuroVault...")

                # Find files
                images = out_dir / 'fitlins'

                ses_dirs = [a for a in images.glob('ses*') if a.is_dir()]
                if ses_dirs:  # If session, look for stat files in session fld
                    images = images / ses_dirs[0]

                group = [i for i in images.glob('task*statmap.nii.gz')
                         if re.match('.*stat-[t|variance|effect]+.*', i.name)]

                sub = [i for i in images.glob('sub*/*statmap.nii.gz')
                       if re.match('.*stat-[variance|effect]+.*', i.name)]

                # Upload results NeuroVault
                self.api.analyses.upload_neurovault(
                    id=self.bundle_id,
                    validation_hash=install.resources['validation_hash'],
                    group_paths=group, subject_paths=sub,
                    force=neurovault == 'force',
                    n_subjects=n_subjects)
        else:
            logging.error(
                "\n"
                "-----------------------------------------------------------\n"
                "Model execution failed! \n"
                f"neuroscout-cli version: {VERSION}\n"
                "Try updating or revising your model, and try again.\n"
                "If you believe there is a bug, please report it:\n"
                "https://github.com/neuroscout/neuroscout-cli/issues\n"
                "-----------------------------------------------------------\n"
                )
