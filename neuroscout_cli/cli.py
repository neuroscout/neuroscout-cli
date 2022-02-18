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
    """Neuroscout-CLI allows you to easily run analyses created on https://neuroscout.org. 
    
    Neuroscout downloads the required data, configures outputs, and uses FitLins to execute analyses. Results
    are automatically uploaded to NeuroVault, facilitating data sharing. 
    
    Note: If using Docker, remember to map local volumes to the container using "-v" (such as OUT_DIR).
    
    For additional help visit: https://neuroscout.github.io/neuroscout/cli/
    """
    pass

@click.argument('out_dir', type=click.Path())
@click.argument('analysis_id')
@click.option('--install-dir', help='Directory to cache input datasets, instead of OUT_DIR', type=click.Path())
@click.option('--upload-first-level', is_flag=True, help='Upload first-level image, in addition to group')
@click.option('--no-upload', is_flag=True, help="Don't automatically upload results to NeuroVault")
@click.option('--force-upload', default=False, is_flag=True, help='Force upload even if a NV collection already exists')
@click.argument('fitlins_args', nargs=-1, type=click.UNPROCESSED)
@main.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_interspersed_args=False
))
def run(**kwargs):
    """ Run an analysis. 
    
    Automatically downloads and configure inputs if you haven't already run "install". Uploads results to
    NeuroVault by default. 
    
    This command uses FitLins for analysis execution. Thus, any valid options can be passed through to FitLins
    in [FITLINS_ARGS]
    """
    sys.exit(ncl.Run(kwargs).run())

  
@click.argument('out_dir', type=click.Path())
@click.argument('analysis_id')
@click.option('--install-dir', help='Directory to cache input datasets, instead of OUT_DIR', type=click.Path())
@main.command()
def install(**kwargs):
    """ Prepare for analysis.
    
    Configures the output directory, and downloads the analysis bundle and 
    required imaging data.
    
    Inputs are downloaded to the output directory under `sourcedata`. If you run many analyses,
    you may wish to provide an `--install-dir` where datasets can be cached across analyses. 
    
    Note: `run` will automatically call `install` prior to execution.
    """
    sys.exit(ncl.Install(kwargs).run())

@click.argument('out_dir', type=click.Path())
@click.argument('analysis_id')
@click.option('--upload-first-level', is_flag=True, help='Upload first-level image, in addition to group')
@click.option('--no-upload', is_flag=True, help="Don't automatically upload results to NeuroVault")
@click.option('--force-upload', default=False, is_flag=True, help='Force upload even if a NV collection already exists')
@main.command()
def upload(**kwargs):
   """ Upload results.
   
   This command can be used to upload results given a completed output directory.
   
   Note: `upload` is by `run` after execution by default.
   """
   sys.exit(ncl.Upload(kwargs).run())
