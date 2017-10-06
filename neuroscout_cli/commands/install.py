from neuroscout_cli.commands.base import Command

from datalad import api as dl
from datalad.auto import AutomagicIO
from os.path import isdir, exists, join
import requests
import json


class Install(Command):

    ''' Command for retrieving neuroscout bundles and data. '''

    def is_bundle_local(self):
        local = isdir(self.bundle_id)
        local = exists(join(self.bundle_id, 'analysis.json'))
        local = exists(join(self.bundle_id, 'design'))
        local = exists(join(self.bundle_id, 'resources.json'))
        return local

    def download_bundle(self):
        if not self.is_bundle_local():
            endpoint = '146.6.123.97/api/analyses/%s/bundle' % self.bundle_id
            bundle = requests.get(endpoint).json()
            print bundle
            ### TODO: write bundle files out to disk

    def download_data(self):
        resources = json.load(join(self.bundle_id, 'resources.json'))
        # Use datalad to get raw BIDS dataset
        bids_dir = resources['dataset_address']
        bids_dir = dl.install(source=bids_dir,
                              path=self.install_dir).path
        automagic = AutomagicIO()
        automagic.activate()

        # Fetch remote preprocessed files
        remote_urls = resources['remote_resources']
        data_dir = join(self.install_dir, bids_dir)
        for url in remote_urls:
            data = requests.get(url).content
            filename = join(data_dir, url.split('/')[-1])
            if not exists(filename):
                with open(filename, 'w') as f:
                    f.write(data)

        return data_dir

    def run(self):
        self.bundle_id = self.options['<bundle_id>']
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
