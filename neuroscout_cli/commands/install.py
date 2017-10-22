from neuroscout_cli.commands.base import Command

from datalad import api as dl
from datalad.auto import AutomagicIO
from os.path import isdir, exists, join
import requests
import json
import tarfile


class Install(Command):

    ''' Command for retrieving neuroscout bundles and their corresponding
    data. '''

    def is_bundle_local(self):
        local = isdir(self.bundle_name)
        local &= exists(join(self.bundle_name, 'resources.json'))
        local &= exists(join(self.bundle_name, 'events.tsv'))
        local &= exists(join(self.bundle_name, 'analysis.json'))
        return local

    def download_bundle(self):
        if not self.is_bundle_local():
            endpoint = 'http://146.6.123.97/api/analyses/%s/bundle' % self.bundle_id
            bundle = requests.get(endpoint)
            tarname = self.bundle_name + '.tar.gz'
            with open(tarname, 'w') as f:
                f.write(bundle.content)

            compressed = tarfile.open(tarname)
            compressed.extractall(self.bundle_name)

    def download_data(self, install_dir):
        # Data addresses are stored in the resources file of the bundle
        with open(join(self.bundle_name, 'resources.json'), 'r') as f:
            resources = json.load(f)

        # Use datalad to get the raw BIDS dataset
        bids_dir = resources['dataset_address']
        bids_dir = dl.install(source=bids_dir,
                              path=install_dir).path
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
        self.bundle_name = self.bundle_id + '_bundle'
        if self.options.pop('bundle'):
            self.download_bundle()
            return self.bundle_name
        elif self.options.pop('data'):
            if not self.is_bundle_local():
                raise Exception("Cannot use [data] option of this command"
                                "unless the bundle is available locally.")
            return self.download_data(self.options['-i'])
        else:
            self.download_bundle()
            return self.bundle_name, self.download_data(self.options['-i'])
