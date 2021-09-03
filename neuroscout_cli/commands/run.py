import logging
import re
import json
from pathlib import Path
from neuroscout_cli.commands.base import Command
from neuroscout_cli import __version__ as VERSION
from neuroscout_cli.commands.install import Install
from fitlins.cli.run import run_fitlins
from bids.layout import BIDSLayout
from datalad.api import drop


class Run(Install):
    ''' Command for running neuroscout workflows. '''

    def run(self, upload_only=False):
        # Download bundle and install dataset if necessary
        super().run(download_data=(not upload_only))
        
        model_path = (self.bundle_dir / 'model.json').absolute()
        neurovault = self.options.pop('--neurovault', 'group')
        nv_force = self.options.pop('--force-neurovault', False)
        no_drop = self.options.pop('--no-datalad-drop', False)
        
        out_dir = self.main_dir
        out_dir.mkdir(exist_ok=True)

        if neurovault not in ['disable', 'group', 'all']:
            raise ValueError("Invalid neurovault option.")

        # Need to retrieve this from fitlins output once it's available
        estimator = None
        if not upload_only:
            fitlins_args = [
                str(self.preproc_dir.absolute()),
                str(out_dir),
                'dataset',
                f'--model={model_path}',
                '--ignore=/(.*desc-confounds_regressors.*)/',
                f'--derivatives={str(self.bundle_dir.absolute())} {str(self.preproc_dir.absolute())}',
                f'--smoothing={self.options["--smoothing"]}:Dataset',
                f'--estimator={self.options["--estimator"]}',
                f'--drop-missing={self.options["--drop-missing"]}'
            ]

            verbose = self.options.pop('--verbose')
            if verbose:
                fitlins_args.append('-vvv')
            work_dir = self.options.pop('--work-dir', None)
            if work_dir:
                work_dir = str(Path(work_dir).absolute() / self.bundle_id)
                fitlins_args.append(f"--work-dir={work_dir}")
                
            # Save options used in execution
            json.dump(self.options, open(out_dir / 'options.json' 'w'))
                        
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

            try:
                fmriprep_version = BIDSLayout(
                    self.preproc_dir).description['PipelineDescription']['Version']
            except Exception:
                fmriprep_version = None

            logging.info("Uploading results to NeuroVault...")

            # Find files
            images = out_dir / 'fitlins'

            ses_dirs = [a for a in images.glob('ses*') if a.is_dir()]
            if ses_dirs:  # If session, look for stat files in session fld
                images = images / ses_dirs[0]

            group = [str(i) for i in images.glob('*statmap.nii.gz')
                     if re.match(
                         '.*stat-(t|F|variance|effect)+.*', i.name)]

            if neurovault == 'all':
                sub = [str(i) for i in images.glob('sub*/*statmap.nii.gz')
                       if re.match('.*stat-(variance|effect)+.*', i.name)]
            else:
                sub = None

            # Upload results NeuroVault
            self.api.analyses.upload_neurovault(
                id=self.bundle_id,
                validation_hash=self.resources['validation_hash'],
                group_paths=group, subject_paths=sub,
                force=nv_force,
                fmriprep_version=fmriprep_version,
                estimator=estimator,
                cli_version=VERSION,
                n_subjects=n_subjects)

        # Drop files if no separate install dir, and the user has not said otherwise.
        if not self.install_dir and not no_drop:
            drop(str(self.preproc_dir.absolute()))