from neuroscout_cli.commands import Install
from neuroscout_cli.commands.base import Command

import os
import subprocess
import tempfile


class Ls(Command):

    ''' Command for displaying a list of available files. '''

    def run(self):
        # Install the needed bundle
        # This command should probably not download the files to list them
        install_command = Install({'bundle': False,
                                   'data': False,
                                   '-i': tempfile.mkdtemp(),
                                   '<bundle_id>': self.options['<bundle_id>']})
        bundle_path, bids_dir = install_command.run()

        cwd = os.getcwd()
        os.chdir(bids_dir)
        subprocess.call(['git', 'ls-files'])
        os.chdir(cwd)
