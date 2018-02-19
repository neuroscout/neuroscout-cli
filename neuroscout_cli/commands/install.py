from neuroscout_cli.commands.base import Command
from neuroscout_cli import API_URL
from datalad.api import install
from pathlib import Path
import requests
import json
import tarfile

class Install(Command):

    ''' Command for retrieving neuroscout bundles and their corresponding
    data. '''

    def is_bundle_local(self):
        local = (self.install_dir / 'bundle').isdir()
        local &= (self.install_dir / 'bundle' / 'resources.json').exists()
        local &= (self.install_dir / 'bundle' / 'events.tsv').exists()
        local &= (self.install_dir / 'bundle' / 'analysis.json').exists()
        return local

    def download_bundle(self):
        if not self.is_bundle_local():
            endpoint = API_URL + 'analyses/{}/bundle'.format(self.bundle_id)
            bundle = requests.get(endpoint)

            tarname = self.install_dir / 'bundle.tar.gz'
            with open(tarname, 'w') as f:
                f.write(bundle.content)

            compressed = tarfile.open(tarname)
            compressed.extractall(self.install_dir / 'bundle')

        return self.bundle_name

    def download_data(self):
        # Data addresses are stored in the resources file of the bundle
        with (self.install_dir / 'bundle' / 'resources.json').open() as f:
            resources = json.load(f)

        # Use datalad to install the raw BIDS dataset
        bids_dir = install(source=resources['dataset_address'],
                           path=self.install_dir.as_posix()).path

        # Pre-fetch specific files from the original dataset?

        # Fetch remote preprocessed files
        remote_path = resources['preproc_address']
        remote_files = resources['func_paths'] + resources['mask_paths']
        for resource in remote_files:
            filename = Path(bids_dir) / 'preproc' / resource
            if not filename.exists():
                url = remote_path + resource
                data = requests.get(url).content
                with filename.open() as f:
                    f.write(data)

        return bids_dir

    def run(self):
        self.bundle_id = self.options['<bundle_id>']
        self.bundle_name = self.bundle_id + '_bundle'
        self.install_dir = Path(self.options.pop('-i'), '.') / self.bundle_name

        if self.options.pop('bundle'):
            return self.download_bundle()
        elif self.options.pop('data'):
            if not self.is_bundle_local():
                raise Exception("Cannot use [data] option of this command"
                                "unless the bundle is available locally.")
            return self.download_data()
        else:
            return self.download_bundle(), self.download_data()
