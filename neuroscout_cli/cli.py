"""
neuroscout-cli
"""

import sys
from copy import deepcopy
from neuroscout_cli import __version__ as VERSION
import logging
import click
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
logging.getLogger().setLevel(logging.INFO)

def fitlins_help(ctx, param, value):
    from fitlins.cli.run import run_fitlins
    if not value or ctx.resilient_parsing:
        return
    run_fitlins(['--help'])
    ctx.exit()

@click.group()
def main():
    """Runs analyses created on https://neuroscout.org. 
    
    Neuroscout-CLI downloads the required data, configures outputs, and uses FitLins to execute analyses. Results
    are automatically uploaded to NeuroVault, facilitating data sharing. 
    
    In most use cases, the "run" command will handle all of the above, although the "get" and "upload" command
    are available for piecemeal execution.
    
    Note: If using Docker, remember to map local volumes to the container using "-v" (such as OUT_DIR).
    
    For additional help visit: https://neuroscout.github.io/neuroscout/cli/
    """
    pass

@click.argument('out_dir', type=click.Path())
@click.argument('analysis_id')
@click.option('--fitlins-help', is_flag=True, callback=fitlins_help, expose_value=False, is_eager=True,
              help='Display FitLins help and options')
@click.option('--no-upload', is_flag=True, help="Don't upload results to NeuroVault")
@click.option('--upload-first-level', is_flag=True, help='Upload first-level results, in addition to group')
@click.option('--force-upload', is_flag=True, help='Force upload even if a NV collection already exists')
@click.option('--no-get', is_flag=True, help="Don't automatically fetch bundle & dataset")
@click.option('--datalad-jobs', help='Number of parallel jobs for DataLad when fetching files', default=1, type=click.INT)
@click.option('--download-dir', help='Directory to cache input datasets, instead of OUT_DIR', type=click.Path())
@click.argument('fitlins_options', nargs=-1, type=click.UNPROCESSED)
@main.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_interspersed_args=False
))
def run(**kwargs):
    """ Run an analysis. 
    
    Automatically gets inputs and uploads results to NeuroVault by default.
    
    This command uses FitLins for execution. Thus, any valid options can be passed through
    in [FITLINS_OPTIONS]. 

    Note: `--model`, `--derivatives` and `--ignore` and positional arguments
    are automatically configured.
    
    Example:

        neuroscout run --force-upload --n-cpus=3 a54oo /out


    If using Docker, remember to map local volumes to save outputs:

        docker run --rm -it -v /local/dir:/out neuroscout/neuroscout-cli run a54oo /out
    """
    from neuroscout_cli.commands import Run
    sys.exit(Run(kwargs).run())

  
@click.argument('out_dir', type=click.Path())
@click.argument('analysis_id')
@click.option('--bundle-only', is_flag=True, help="Only fetch analysis bundle, not imaging data")
@click.option('--download-dir', help='Directory to cache input datasets, instead of OUT_DIR', type=click.Path())
@click.option('--datalad-jobs', help='Number of parallel jobs for DataLad when fetching files', default=1, type=click.INT)
@main.command()
def get(**kwargs):
    """ Fetch analysis inputs.
    
    Downloads the analysis bundle, preprocessed fMRI inputs, and configures output directory.
    
    Inputs are downloaded to the output directory under `sourcedata`. If you run many analyses,
    you may wish to provide an `--download-dir` where datasets can be cached across analyses. 
    
    Note: `run` automatically calls `get` prior to execution, by default.
    """
    from neuroscout_cli.commands import Get
    sys.exit(Get(kwargs).run())

@click.argument('out_dir', type=click.Path())
@click.argument('analysis_id')
@click.option('--upload-first-level', is_flag=True, help='Upload first-level results, in addition to group')
@click.option('--force-upload', is_flag=True, help='Force upload even if a NV collection already exists')
@main.command()
def upload(**kwargs):
   """ Upload results.
   
   This command can be used to upload existing results to NeuroVault.
   
   Note: `run` automatically calls `upload` after execution, by default.
   """
   from neuroscout_cli.commands import Upload
   sys.exit(Upload(kwargs).run())
