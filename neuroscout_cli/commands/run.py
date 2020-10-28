from neuroscout_cli.commands.base import Command
from neuroscout_cli import __version__ as VERSION
from neuroscout_cli.commands.install import Install
from fitlins.cli.run import run_fitlins
from bids.layout import BIDSLayout
from pathlib import Path
import logging
import re
import json

# Options not to be passed onto fitlins
INVALID = ['--unlock', '--version', '--help', '--install-dir',
           'run', '<bundle_id>', '--dataset-name']


class Run(Command):
    ''' Command for running neuroscout workflows. '''

    def run(self, upload_only=False):
        # Download bundle and install dataset if necessary
        install = Install(self.options.copy())
        bundle_path = install.run(download_data=(not upload_only))

        out_dir = Path(self.options.pop('<outdir>')) / install.bundle_id
        model_path = (bundle_path / 'model.json').absolute()
        neurovault = self.options.pop('--neurovault', 'group')
        nv_force = self.options.pop('--force-neurovault', False)
        preproc_path = str(install.preproc_dir.absolute())

        if neurovault not in ['disable', 'group', 'all']:
            raise ValueError("Invalid neurovault option.")

        if not upload_only:
            smoothing = self.options.pop('--smoothing')

            fitlins_args = [
                preproc_path,
                str(out_dir),
                'dataset',
                f'--model={model_path}',
                '--ignore=/(.*desc-confounds_regressors.tsv)/',
                f'--derivatives={bundle_path} {preproc_path}',
                f'--smoothing={smoothing}:Dataset'
            ]

            verbose = self.options.pop('--verbose')
            if verbose:
                fitlins_args.append('-vvv')
            work_dir = self.options.pop('--work-dir', None)
            if work_dir:
                work_dir = str(Path(work_dir).absolute() / self.bundle_id)
                fitlins_args.append(f"--work-dir={work_dir}")

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

            if retcode != 0:
                logging.error(
                    "\n"
                    "-------------------------------------------------------\n"
                    "Model execution failed! \n"
                    f"neuroscout-cli version: {VERSION}\n"
                    "Update neuroscout-cli or revise your model, "
                    "and try again \n"
                    "If you believe there is a bug, please report it:\n"
                    "https://github.com/neuroscout/neuroscout-cli/issues\n"
                    "-------------------------------------------------------\n"
                    )

        if neurovault != 'disable':
            model = json.load(open(model_path, 'r'))
            n_subjects = len(model['Input']['Subject'])

            fmriprep_version = BIDSLayout(
                preproc_path).description['PipelineDescription']['Version']

            logging.info("Uploading results to NeuroVault...")

            # Find files
            images = out_dir / 'fitlins'

            ses_dirs = [a for a in images.glob('ses*') if a.is_dir()]
            if ses_dirs:  # If session, look for stat files in session fld
                images = images / ses_dirs[0]

            group = [str(i) for i in images.glob('task*statmap.nii.gz')
                     if re.match(
                         '.*stat-[t|F|variance|effect]+.*', i.name)]

            if neurovault == 'all':
                sub = [str(i) for i in images.glob('sub*/*statmap.nii.gz')
                       if re.match('.*stat-[variance|effect]+.*', i.name)]
            else:
                sub = None

            # Upload results NeuroVault
            self.api.analyses.upload_neurovault(
                id=self.bundle_id,
                validation_hash=install.resources['validation_hash'],
                group_paths=group, subject_paths=sub,
                force=nv_force,
                fmriprep_version=fmriprep_version,
                cli_version=VERSION,
                n_subjects=n_subjects)
