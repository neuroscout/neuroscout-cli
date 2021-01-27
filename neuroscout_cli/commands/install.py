import json
import tarfile
import logging
import sys

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
        self.install_dir = Path(self.options.pop('--install-dir'))

    def download_bundle(self):
        # Download bundle
        if not self.bundle_cache.exists():
            logging.info("Downloading bundle...")
            self.api.analyses.get_bundle(self.bundle_id, self.bundle_cache)

        # Un-tarzip, and read in JSON files
        with tarfile.open(self.bundle_cache) as tF:
            self.resources = json.loads(
                tF.extractfile('resources.json').read().decode("utf-8"))

            self.dataset_dir = self.install_dir / \
                self.resources['dataset_name']
            self.bundle_dir = self.dataset_dir \
                / 'neuroscout-bundles' / self.bundle_id

            #  Extract to bundle_dir
            if not self.bundle_dir.exists():
                self.bundle_dir.mkdir(parents=True, exist_ok=True)
                tf.extractall(self.bundle_dir)
                logging.info(
                    "Bundle installed at {}".format(
                        self.bundle_dir.absolute()))

        # Set up preproc dir w/ DataLad (but don't download)
        self.preproc_dir = Path(self.dataset_dir) / 'derivatives'

        if not self.preproc_dir.exists():
            # Use datalad to install the preproc dataset
            install(source=self.resources['preproc_address'],
                    path=str(self.preproc_dir))

        for option in ['preproc', 'fmriprep']:
            if (self.preproc_dir / option).exists():
                self.preproc_dir = self.preproc_dir / option
                break

        # Check version
        self._check_version()

        return self.bundle_dir.absolute()

    def download_data(self):
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
                raise(exp)

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
                f"This bundle requires v{str(req)} or greater, and you current have v{VERSION} \n"
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
