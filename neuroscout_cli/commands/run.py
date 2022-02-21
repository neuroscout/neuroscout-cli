import logging
import json
from pathlib import Path
from re import L
from textwrap import indent
from neuroscout_cli.commands.get import Get
from neuroscout_cli.commands.upload import Upload
from neuroscout_cli import __version__ as VERSION
from fitlins.cli.run import run_fitlins


class Run(Get):
    ''' Command for running neuroscout workflows. '''

    def run(self):
        # Download bundle and get dataset if necessary
        if not self.options['no_get']:
            retcode = super().run()
        
        # Need to retrieve this from fitlins output once it's available
        fitlins_args = [
            str(self.preproc_dir),
            str(self.main_dir),
            'dataset',
            f'--model={str(self.model_path.absolute())}',
            '--ignore=/(.*desc-confounds_regressors.*)/',
            f'--derivatives={str(self.bundle_dir.absolute())} {str(self.preproc_dir.absolute())}',
        ]
        
        # Append pass through options
        fitlins_args+= list(self.options['fitlins_options'])
            
        # Save options used in execution
        json.dump(
            self.options, (self.main_dir / 'options.json').open('w'),
            indent=4
            )
                    
        # Call fitlins as if CLI
        retcode = run_fitlins(fitlins_args)

        if retcode != 0:
            logging.error(
                "\n"
                "-------------------------------------------------------\n"
                "Model execution failed! \n"
                f"neuroscout-cli version: {VERSION}\n"
                "Update neuroscout-cli or revise your model, and try again \n"
                "If you believe there is a bug, please report it:\n"
                "https://github.com/neuroscout/neuroscout-cli/issues\n"
                "-------------------------------------------------------\n"
                )
            return retcode

        if not self.options['no_upload']:
            # Upload results
            up = Upload(self.options)
            up.run(preproc_dir=self.preproc_dir)
        
        return retcode