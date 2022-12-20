import json
import tarfile
import logging
import sys
import datalad

from pathlib import Path
from shutil import copy
from packaging import version
from neuroscout_cli.commands.base import Command
from neuroscout_cli import __version__ as VERSION
from bids.utils import convert_JSON
from ..tools.convert import check_convert_mode
from pyns.fetch_utils import fetch_images

datalad.ui.ui.set_backend('console')
                          
class Get(Command):

    ''' Command for retrieving neuroscout bundles and their corresponding
    data. '''

    def __init__(self, options):
        super().__init__(options)
        self.download_dir = self.options.get('download_dir', None)
        if self.download_dir is not None:
            self.download_dir = Path(self.download_dir)
        else:
            self.download_dir = self.main_dir / 'sourcedata'
            
        # Make dirs
        self.main_dir.mkdir(parents=True, exist_ok=True)
        self.bundle_dir.mkdir(parents=True, exist_ok=True)        

    def download(self, no_get=False):
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
                    "Bundle installed at %s", self.bundle_dir
                )
                
        self.model_path = check_convert_model(
            (self.bundle_dir / 'model.json').absolute()   
            ) # Convert if necessary

        # Load model
        with self.model_path.open() as f:
            model = convert_JSON(json.load(f))

        self.preproc_dir, paths = fetch_images(
            self.resources['dataset_name'], self.dataset_dir, no_get=no_get, 
            preproc_address=self.resources['preproc_address'],
            datalad_jobs=self.options.get('datalad_jobs', -1),
            fetch_json=True, fetch_brain_mask=True, **model['input'])

        self.dataset_dir = self.preproc_dir.parent

        if not no_get:
            # Copy meta-data to root of preproc_dir
            meta = list(self.bundle_dir.glob('task-*json'))[0]
            if not (self.preproc_dir/ meta.parts[-1]).exists():
                copy(meta, self.preproc_dir)

        return 0
    
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

    def run(self, no_get=False):
        bundle_only = self.options.get('bundle_only', False)
        if bundle_only:
            no_get = True
        retcode = self.download(no_get=no_get)
            
        return retcode

