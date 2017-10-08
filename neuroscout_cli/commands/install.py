from neuroscout_cli.commands.base import Command

from datalad import api as dl
from datalad.auto import AutomagicIO
from os.path import isdir, exists, join
import requests
import json


class Install(Command):

    ''' Command for retrieving neuroscout bundles and their corresponding
    data. '''

    def is_bundle_local(self):
        local = isdir(self.bundle_id)
        local = exists(join(self.bundle_id, 'resources'))
        local = exists(join(self.bundle_id, 'events'))
        local = exists(join(self.bundle_id, 'full'))
        return local

    def download_bundle(self):
        if not self.is_bundle_local():
            endpoint = 'http://146.6.123.97/api/analyses/%s/bundle' % self.bundle_id
            ### TODO: use tarball endpoint
            bundle = requests.get(endpoint).json()
            with open(self.bundle_filename, 'w') as f:
                json.dump(bundle, f)

    def download_data(self):
        # Data addresses are stored in the resources file of the bundle
        with open(join(self.bundle_id, 'resources'), 'r') as f:
            resources = json.load(f)

        # Use datalad to get the raw BIDS dataset
        bids_dir = resources['dataset_address']
        bids_dir = dl.install(source=bids_dir,
                              path=self.install_dir).path
        automagic = AutomagicIO()
        automagic.activate()

        # Fetch remote preprocessed files
        remote_path = resources['preproc_address']
        remote_files = resources['func_paths'] + resources['mask_paths']
        for resource in remote_files:
            filename = join(bids_dir, resource)
            if not exists(filename):
                url = remote_path + resource
                data = requests.get(url).content
                with open(filename, 'w') as f:
                    f.write(data)

        return bids_dir

    def run(self):
        self.bundle_id = self.options['<bundle_id>']
        self.install_dir = self.options['-i']
        if self.options.pop('bundle'):
            self.download_bundle()
            return self.bundle_id
        elif self.options.pop('data'):
            if not self.is_bundle_local():
                raise Exception("Cannot use [data] option of this command"
                                "unless the bundle is available locally.")
            return self.download_data()
        else:
            self.download_bundle()
            return self.bundle_id, self.download_data()
