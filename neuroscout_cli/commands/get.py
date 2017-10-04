from neuroscout_cli.commands.base import Command

from datalad import api as dl
from datalad.auto import AutomagicIO
import httplib
import json
import os.path


class Get(Command):

    ''' Command for retrieving neuroscout bundles and data. '''

    def is_bundle_local(self):
        ''' Checks if full bundle is downloaded locally. '''
        bid = self.options['bundle_id']
        exists = os.path.isdir(bid)
        exists = os.path.exists(os.path.join(bid, 'analysis.json'))
        exists = os.path.exists(os.path.join(bid, 'design'))
        exists = os.path.exists(os.path.join(bid, 'resources.json'))
        return exists

    def download_bundle(self):
        if not self.is_bundle_local():
            conn = httplib.HTTPSConnection('146.6.123.97')
            conn.request('GET', '/api/analyses/%s/bundle' % self.options['bundle_id'])
            response = conn.getresponse()
            bundle = json.loads(response.read())
            conn.close()
            print bundle
            # TODO: write bundle files out to disk

    def download_data(self):
        # TODO: fix this
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
