from neuroscout_cli.commands.base import Command

from datalad import api as dl
from datalad.auto import AutomagicIO
from os.path import isdir, exists, join
import httplib
import json


class Get(Command):

    ''' Command for retrieving neuroscout bundles and data. '''

    def is_bundle_local(self):
        local = isdir(self.bundle_id)
        local = exists(join(self.bundle_id, 'analysis.json'))
        local = exists(join(self.bundle_id, 'design'))
        local = exists(join(self.bundle_id, 'resources.json'))
        return local

    def download_bundle(self):
        if not self.is_bundle_local():
            conn = httplib.HTTPSConnection('146.6.123.97')
            conn.request('GET', '/api/analyses/%s/bundle' % self.bundle_id)
            response = conn.getresponse()
            bundle = json.loads(response.read())
            conn.close()
            print bundle
            # TODO: write bundle files out to disk

    def download_data(self):
        resources = json.load(join(self.bundle_id, 'resources.json'))
        print resources
        # TODO: fix this to actually use resources
        if not self.options['-i'] and self.options['-b']:
            bids_dir = dl.install(path=self.options['bids_dir']).path
        else:
            if not self.options['-i']:
                self.options['-i'] = self.options['work_dir']
            bids_dir = dl.install(source=bids_dir,
                                  path=self.options['-i']).path

        automagic = AutomagicIO()
        automagic.activate()

    def run(self):
        self.bundle_id = self.options['bundle_id']
        if self.options.pop('bundle'):
            self.download_bundle()
        elif self.options.pop('data'):
            if not self.is_bundle_local():
                raise Exception("Cannot use [data] option of this command"
                                "unless the bundle is available locally.")
            self.download_data()
        else:
            self.download_bundle()
            self.download_data()
