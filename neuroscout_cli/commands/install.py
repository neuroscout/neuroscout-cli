from neuroscout_cli.commands.base import Command

from datalad import api as dl
from datalad.auto import AutomagicIO
from os.path import exists, join
import requests
import json


class Install(Command):

    ''' Command for retrieving neuroscout bundles and their corresponding
    data. '''

    def is_bundle_local(self):
        local = exists(self.bundle_filename)
        return local

    def download_bundle(self):
        if not self.is_bundle_local():
            endpoint = 'http://146.6.123.97/api/analyses/%s/bundle' % self.bundle_id
            bundle = requests.get(endpoint).json()
            with open(self.bundle_filename, 'w') as f:
                json.dump(bundle, f)

    def download_data(self):
        # resources = json.load(join(self.bundle_id, 'resources.json'))
        with open(self.bundle_filename, 'r') as f:
            bundle = json.load(f)

        # Use datalad to get raw BIDS dataset
        bids_dir = bundle['dataset_address']
        bids_dir = dl.install(source=bids_dir,
                              path=self.install_dir).path
        automagic = AutomagicIO()
        automagic.activate()

        # Fetch remote preprocessed files
        remote_path = bundle['preproc_address']
        remote_files = [r['func_path'] for r in bundle['runs']]
        for preprocessed_file in remote_files:
            url = remote_path + preprocessed_file
            data = requests.get(url).content
            filename = join(bids_dir, preprocessed_file)
            if not exists(filename):
                with open(filename, 'w') as f:
                    f.write(data)

        return bids_dir

    def run(self):
        self.bundle_id = self.options['<bundle_id>']
        self.bundle_filename = '%s.json' % self.bundle_id
        self.install_dir = self.options['-i']
        if self.options.pop('bundle'):
            self.download_bundle()
        elif self.options.pop('data'):
            if not self.is_bundle_local():
                raise Exception("Cannot use [data] option of this command"
                                "unless the bundle is available locally.")
            return self.download_data()
        else:
            self.download_bundle()
            return self.download_data()
