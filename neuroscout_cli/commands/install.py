from neuroscout_cli.commands.base import Command
from neuroscout_cli import API_URL
from datalad.api import install
from pathlib import Path
import requests
import json
import tarfile
import logging

class Install(Command):

    ''' Command for retrieving neuroscout bundles and their corresponding
    data. '''
    def download_bundle(self):
        if not self.bundle_cache.exists():
            logging.info("Downloading bundle...")
            endpoint = API_URL + 'analyses/{}/bundle'.format(self.bundle_id)
            bundle = requests.get(endpoint)

            if bundle.status_code != 200:
                if json.loads(bundle.content)['message'] == 'Resource not found':
                    raise Exception("Bundle could not be found. Check your spelling and try again.")
                raise Exception("Error fetching bundle.")

            with self.bundle_cache.open('wb') as f:
                f.write(bundle.content)

        tf = tarfile.open(self.bundle_cache)
        self.resources = json.loads(tf.extractfile('resources.json').read().decode("utf-8"))

        ## Need to add dataset name to resouces for folder name
        self.dataset_dir = self.install_dir / self.resources['dataset_name']
        self.bundle_dir = self.dataset_dir / 'derivatives' / 'neuroscout' / self.bundle_id

        ## Probably need to add option to force-redownload
        if not self.bundle_dir.exists():
            self.bundle_dir.mkdir(parents=True, exist_ok=True)
            tf.extractall(self.bundle_dir)
            print("Bundle installed at {}".format(self.bundle_dir.absolute()))

        return self.bundle_dir.absolute()

    def download_data(self):
        self.download_bundle()
        logging.info("Installing dataset...")
        # Use datalad to install the raw BIDS dataset
        install(source=self.resources['dataset_address'],
                path=(self.dataset_dir).as_posix()).path

        # Pre-fetch specific files from the original dataset?
        logging.info("Fetching remote resources...")

        # Fetch remote preprocessed files
        remote_path = self.resources['preproc_address']
        remote_files = self.resources['func_paths'] + self.resources['mask_paths']

        preproc_dir = Path(self.dataet_dir) / 'derivatives' / 'fmriprep'
        preproc_dir.mkdir(exist_ok=True, parents=True)

        for resource in remote_files:
            filename = preproc_dir / resource
            if not filename.exists():
                url = remote_path + resource
                data = requests.get(url).content
                with filename.open() as f:
                    f.write(data)

        return self.dataset_dir

    def run(self):
        self.bundle_id = self.options['<bundle_id>']
        self.bundle_cache = (self.home / self.bundle_id).with_suffix(".tar.gz")
        self.install_dir = Path(self.options.pop('-i'))

        if self.options.pop('bundle'):
            return self.download_bundle()
        elif self.options.pop('data'):
            return self.download_data()
        else:
            return self.download_data()
