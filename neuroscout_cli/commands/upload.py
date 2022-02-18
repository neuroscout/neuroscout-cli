import logging
import json
import re
from bids.layout import BIDSLayout
from neuroscout_cli.commands.base import Command
from neuroscout_cli import __version__ as VERSION


class Upload(Command):
    ''' Command for running neuroscout workflows. '''

    def __init__(self, options):
        super().__init__(options)

    def run(self, preproc_dir=None):
        subject_level = self.options.get('--upload-first-level', False)
        nv_force = self.options.get('--force-upload', False)
        resources = json.load((self.bundle_dir / 'resources.json').open())
        
        model = json.load(open(self.model_path, 'r'))
        n_subjects = len(model['Input']['Subject'])
        
        # Load esimator from file in case of upload only
        try:
            saved_options = json.load((self.main_dir / 'options.json').open('r'))
            estimator = saved_options.get('--estimator')
        except:
            estimator = None
            saved_options = None
            print("No saved options found skipping...")

        fmriprep_version = None
        if preproc_dir:
            try:
                fmriprep_version = BIDSLayout(
                    preproc_dir).description['PipelineDescription']['Version']
            except Exception:
                pass

        logging.info("Uploading results to NeuroVault...")

        # Find files
        images = self.main_dir / 'fitlins'

        ses_dirs = [a for a in images.glob('ses*') if a.is_dir()]
        if ses_dirs:  # If session, look for stat files in session fld
            images = images / ses_dirs[0]

        group = [str(i) for i in images.glob('*statmap.nii.gz')
                    if re.match(
                        '.*stat-(t|F|variance|effect)+.*', i.name)]

        if subject_level:
            sub = [str(i) for i in images.glob('sub*/*statmap.nii.gz')
                    if re.match('.*stat-(variance|effect)+.*', i.name)]
        else:
            sub = None

        # Upload results NeuroVault
        self.api.analyses.upload_neurovault(
            id=self.bundle_id,
            validation_hash=resources['validation_hash'],
            group_paths=group, subject_paths=sub,
            force=nv_force,
            fmriprep_version=fmriprep_version,
            estimator=estimator,
            cli_version=VERSION,
            cli_args=saved_options,
            n_subjects=n_subjects)
