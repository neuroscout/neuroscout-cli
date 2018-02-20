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

    def is_bundle_local(self):
        local = (self.bundle_dir).is_dir()
        local &= (self.bundle_dir / 'resources.json').exists()
        local &= len(list(self.bundle_dir.glob('*events.tsv'))) > 0
        local &= (self.bundle_dir / 'analysis.json').exists()
        return local

    def download_bundle(self):
        if not self.is_bundle_local():
            logging.info("Downloading bundle...")
            endpoint = API_URL + 'analyses/{}/bundle'.format(self.bundle_id)
            bundle = requests.get(endpoint)

            self.bundle_dir.mkdir()

            tarname = self.bundle_dir / 'bundle.tar.gz'
            with tarname.open() as f:
                f.write(bundle.content)

            compressed = tarfile.open(tarname)
            compressed.extractall(self.bundle_dir)

        return self.bundle_dir

    def download_data(self):
        # Data addresses are stored in the resources file of the bundle
        with (self.bundle_dir / 'resources.json').open() as f:
            resources = json.load(f)

        logging.info("Installing dataset...")
        # Use datalad to install the raw BIDS dataset
        bids_dir = install(source=resources['dataset_address'],
                           path=(self.install_dir/'dataset').as_posix()).path

        # Pre-fetch specific files from the original dataset?

        logging.info("Fetching remote resources...")

        # Fetch remote preprocessed files
        remote_path = resources['preproc_address']
        remote_files = resources['func_paths'] + resources['mask_paths']

        preproc_dir = Path(bids_dir) / 'derivatives' / 'preproc'
        preproc_dir.mkdir(exist_ok=True, parents=True)

        for resource in remote_files:
            filename = preproc_dir / resource
            if not filename.exists():
                url = remote_path + resource
                data = requests.get(url).content
                with filename.open() as f:
                    f.write(data)

        return bids_dir

    def run(self):
        self.bundle_id = self.options['<bundle_id>']
        self.install_dir = Path(self.options.pop('-i'), '.') / self.bundle_id
        self.bundle_dir = self.install_dir /  'bundle'


        if self.options.pop('bundle'):
            return self.download_bundle()
        elif self.options.pop('data'):
            if not self.is_bundle_local():
                raise Exception("Cannot use [data] option of this command"
                                "unless the bundle is available locally.")
            return self.download_data()
        else:
            return self.download_bundle(), self.download_data()
