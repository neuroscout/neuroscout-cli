import logging
import json
from pathlib import Path
from neuroscout_cli.commands import Install, Upload
from neuroscout_cli import __version__ as VERSION
from fitlins.cli.run import run_fitlins


class Run(Install):
    ''' Command for running neuroscout workflows. '''

    def run(self):
        # Download bundle and install dataset if necessary
        retcode = super().run()
        
        # Need to retrieve this from fitlins output once it's available
        fitlins_args = [
            str(self.preproc_dir),
            str(self.main_dir),
            'dataset',
            f'--model={self.model_path}',
            '--ignore=/(.*desc-confounds_regressors.*)/',
            f'--derivatives={str(self.bundle_dir)} {str(self.preproc_dir)}',
            f'--smoothing={self.options["--smoothing"]}',
            f'--estimator={self.options["--estimator"]}',
            f'--n-cpus={self.options["--n-cpus"]}'
        ]

        verbose = self.options.pop('--verbose')
        if verbose:
            fitlins_args.append('-vvv')
        work_dir = self.options.pop('--work-dir', None)
        if work_dir:
            work_dir = str(Path(work_dir).absolute() / self.bundle_id)
            fitlins_args.append(f"--work-dir={work_dir}")
            
        if self.options["--drop-missing"]:
            fitlins_args.append(f"--drop-missing")
            
        # Save options used in execution
        json.dump(self.options, (self.main_dir / 'options.json').open('w'))
                    
        # Call fitlins as if CLI
        retcode = run_fitlins(fitlins_args)

        if retcode != 0:
            logging.error(
                "\n"
                "-------------------------------------------------------\n"
                "Model execution failed! \n"
                f"neuroscout-cli version: {VERSION}\n"
                "Update neuroscout-cli or revise your model, "
                "and try again \n"
                "If you believe there is a bug, please report it:\n"
                "https://github.com/neuroscout/neuroscout-cli/issues\n"
                "-------------------------------------------------------\n"
                )
            return retcode

        # Instatiate Upload commmand with current options, and then run
        up = Upload(self.options)
        up.run(preproc_dir=self.preproc_dir)
        
        return retcode