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
import neuroscout_cli.commands as ncl
logging.getLogger().setLevel(logging.INFO)


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
@click.option('--download-dir', help='Directory to cache input datasets, instead of OUT_DIR', type=click.Path())
@click.option('--no-get', is_flag=True, help="Don't automatically fetch bundle & dataset")
@click.option('--upload-first-level', is_flag=True, help='Upload first-level results, in addition to group')
@click.option('--no-upload', is_flag=True, help="Don't upload results to NeuroVault")
@click.option('--force-upload', default=False, is_flag=True, help='Force upload even if a NV collection already exists')
@click.argument('fitlins_args', nargs=-1, type=click.UNPROCESSED)
@main.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_interspersed_args=False
))
def run(**kwargs):
    """ Run an analysis. 
    
    This command uses FitLins for analysis execution. Thus, any valid options can be passed through to FitLins
    in [FITLINS_ARGS]. Note: FitLins' `--model`, `--derivatives` and `--ignore` options are automatically 
    configured.
    
    By default, automatically gets inputs (if you haven't already run "get") and uploads results
    to NeuroVault ("upload" command).
    
    Example:
        neuroscout run --upload-first-level --n-cpus=3 a54oo /out
    """
    sys.exit(ncl.Run(kwargs).run())

  
@click.argument('out_dir', type=click.Path())
@click.argument('analysis_id')
@click.option('--download-dir', help='Directory to cache input datasets, instead of OUT_DIR', type=click.Path())
@click.option('--bundle-only', is_flag=True, help="Only fetch analysis bundle, not imaging data")
@main.command()
def get(**kwargs):
    """ Fetch analysis inputs.
    
    Downloads the analysis bundle, preprocessed fMRI inputs, and configures output directory.
    
    Inputs are downloaded to the output directory under `sourcedata`. If you run many analyses,
    you may wish to provide an `--download-dir` where datasets can be cached across analyses. 
    
    Note: `run` automatically calls `get` prior to execution, by default.
    """
    sys.exit(ncl.Get(kwargs).run())

@click.argument('out_dir', type=click.Path())
@click.argument('analysis_id')
@click.option('--upload-first-level', is_flag=True, help='Upload first-level results, in addition to group')
@click.option('--no-upload', is_flag=True, help="Don't upload results to NeuroVault")
@click.option('--force-upload', default=False, is_flag=True, help='Force upload even if a NV collection already exists')
@main.command()
def upload(**kwargs):
   """ Upload results.
   
   This command can be used to upload existing results to NeuroVault.
   
   Note: `run` automatically calls `upload` after execution, by default.
   """
   sys.exit(ncl.Upload(kwargs).run())
