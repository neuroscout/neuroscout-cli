from neuroscout_cli.commands.base import Command
from datalad.api import install, get, unlock
from pathlib import Path
from shutil import copy
import requests
import json
import tarfile
import logging
from tqdm import tqdm
from bids.utils import convert_JSON
from bids import BIDSLayout

def download_file(url, path):
    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)

    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    with open(path, 'wb') as f:
        with tqdm(total=total_size, unit='B',
                  unit_scale=True, unit_divisor=1024) as pbar:
            for data in r.iter_content(32*1024):
                f.write(data)
                pbar.update(len(data))


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
            self.api.analyses.bundle(self.bundle_id, self.bundle_cache)

        # Un-tarzip, and read in JSON files
        tf = tarfile.open(self.bundle_cache)
        self.resources = json.loads(
            tf.extractfile('resources.json').read().decode("utf-8"))

        self.dataset_dir = self.install_dir / self.resources['dataset_name']
        self.bundle_dir = self.dataset_dir \
            / 'neuroscout-bundles' / self.bundle_id

        #  Extract to bundle_dir
        if not self.bundle_dir.exists():
            self.bundle_dir.mkdir(parents=True, exist_ok=True)
            tf.extractall(self.bundle_dir)
            logging.info(
                "Bundle installed at {}".format(self.bundle_dir.absolute()))

        return self.bundle_dir.absolute()

    def download_data(self):
        bundle_dir = self.download_bundle()
        with (bundle_dir / 'model.json').open() as f:
            model = convert_JSON(json.load(f))

        self.preproc_dir = Path(self.dataset_dir) / 'preproc' / 'fmriprep'

        try:
            if not self.preproc_dir.parents[0].exists():
                # Use datalad to install the preproc dataset
                install(source=self.resources['preproc_address'],
                        path=str(self.preproc_dir.parents[0]))

            get(str(self.preproc_dir / 'dataset_description.json'))

            layout = BIDSLayout(self.preproc_dir, derivatives=self.preproc_dir)

            paths = layout.get(
                **model['input'], desc='preproc', return_type='file')
            paths += layout.get(
                **model['input'],
                desc='brain', suffix='mask', return_type='file')

            get(paths)

            if self.options.pop('--unlock', False):
                unlock(paths)

        except Exception as e:
            message = e.failed[0]['message']
            raise ValueError("Datalad failed. Reason: {}".format(message))

        # Copy meta-data to root of dataset_dir
        copy(list(self.bundle_dir.glob('task-*json'))[0], self.preproc_dir)

        return self.bundle_dir.absolute()

    def run(self):
        if self.options.pop('--no-download', False):
            return self.download_bundle()
        else:
            return self.download_data()
