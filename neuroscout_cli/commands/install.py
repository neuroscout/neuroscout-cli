import json
import tarfile
import logging
import sys
import tempfile

from pathlib import Path
from shutil import copy
from packaging import version
from neuroscout_cli.commands.base import Command
from neuroscout_cli import __version__ as VERSION
from datalad.api import install, get, unlock
from bids.utils import convert_JSON
from bids import BIDSLayout


class Install(Command):

    ''' Command for retrieving neuroscout bundles and their corresponding
    data. '''

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.resources = None
        self.preproc_dir = None
        self.install_dir = self.options.pop('--install-dir')
        if self.install_dir is not None:
            self.install_dir = Path(self.install_dir)
        self.main_dir = Path(self.options.pop('<outdir>')) / f'neuroscout-{self.bundle_id}'
        self.main_dir.mkdir(parents=True, exist_ok=True)
        
        self.bundle_dir = self.main_dir / 'inputs' / 'bundle'
        self.bundle_dir.mkdir(parents=True, exist_ok=True)

    def download_bundle(self):
        """ Download analysis bundle and setup preproc dir """
        # If tarball doesn't exist, download it
        bundle_tarball = self.bundle_dir / f'{self.bundle_id}.tar.gz'
        if not bundle_tarball.exists():
            logging.info("Downloading bundle...")
            self.api.analyses.get_bundle(self.bundle_id, bundle_tarball)

        # Un-tarzip, and read in JSON files, and extract if needed
        with tarfile.open(bundle_tarball) as tF:
            self.resources = json.loads(
                tF.extractfile('resources.json').read().decode("utf-8"))

            # Check version
            self._check_version()

            #  Extract to bundle_dir
            if not (self.bundle_dir / 'model.json').exists():
                tF.extractall(self.bundle_dir)
                logging.info(
                    "Bundle installed at %s", self.bundle_dir.absolute()
                )
                
        # If cache dir is defind, download there
        if self.install_dir:
            download_dir = self.install_dir
        else:
            download_dir = self.main_dir / 'inputs'
            
        self.preproc_dir = download_dir / self.resources['dataset_name']

        # Install DataLad dataset if dataset_dir does not exist
        if not self.preproc_dir.exists():
            # Use datalad to install the preproc dataset
            install(source=self.resources['preproc_address'],
                    path=str(self.preproc_dir))

        # Set preproc dir to specific directory, depending on contents
        for option in ['preproc', 'fmriprep']:
            if (self.preproc_dir / option).exists():
                self.preproc_dir = self.preproc_dir / option
                break

        return self.bundle_dir.absolute()

    def download_data(self):
        """ Use DataLad to download necessary data to disk """
        bundle_dir = self.download_bundle()
        with (bundle_dir / 'model.json').open() as f:
            model = convert_JSON(json.load(f))

        try:
            # Get all JSON files
            jsons = list(self.preproc_dir.rglob('*.json'))
            if jsons:
                get([str(p) for p in self.preproc_dir.rglob('*.json')])

            layout = BIDSLayout(
                self.preproc_dir,
                derivatives=self.preproc_dir, index_metadata=False)

            paths = layout.get(
                **model['input'], desc='preproc', return_type='file')
            paths += layout.get(
                **model['input'],
                desc='brain', suffix='mask', return_type='file')

            get(paths)

            if self.options.pop('--unlock', False):
                unlock(paths)

        except Exception as exp:
            if hasattr(exp, 'failed'):
                message = exp.failed[0]['message']
                raise ValueError("Datalad failed. Reason: {}".format(message))
            else:
                raise exp

        # Copy meta-data to root of dataset_dir
        copy(list(self.bundle_dir.glob('task-*json'))[0], self.preproc_dir)

        return self.bundle_dir.absolute()

    def _check_version(self):

        # Check version
        req = self.resources.get('version_required', 0.3)
        if version.parse(VERSION) < version.parse(req):
            logging.error(
                "\n"
                "-----------------------------------------------------------\n"
                "Insufficient version of neurosout-cli! \n"
                f"This bundle requires v{str(req)}+, and you have v{VERSION}\n"
                "Please upgrade neuroscout-cli by running: \n"
                "'docker pull neuroscout/neuroscout-cli' to continue. \n"
                "-----------------------------------------------------------\n"
                )
            sys.exit(1)

    def run(self, download_data=True):
        if download_data:
            return self.download_data()
        else:
            return self.download_bundle()
