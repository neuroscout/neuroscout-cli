"""
neuroscout-cli

Usage:
    neuroscout run [options] <outdir> <bundle_id> [<fitlins_args>...]
    neuroscout install [--install-dir <dir>] <outdir> <bundle_id>
    neuroscout upload [--force-upload --neurovault <nv>] <outdir> <bundle_id>
    neuroscout -h | --help
    neuroscout --version

Options:
    --install-dir <dir>  Optional directory to cache input datasets
    --neurovault <nv>    Upload mode (disable, all, or group)
                         [default: group]
    --force-upload       Force upload, if a NV collection already exists
    
Commands:
    run                      Runs analysis using FitLins. Installs inputs & uploads results automatically. 
                             You can pass arbitrary arguments to FitLins after the <bundle_id>.
    install                  Installs a bundle and/or dataset without executing analysis.
    upload                   Upload existing analysis results to Neurovault.

Example:
    neuroscout run --force-upload 5xhaS /out --n-cpus=10

Help:
    For help using neuroscout, visit https://neuroscout.github.io/neuroscout/cli/
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
    # CLI entry point
    # for (k, val) in args.items():
    #     if hasattr(ncl, k) and val:
    #         k = k[0].upper() + k[1:]
    #         command = getattr(ncl, k)
    #         bundle = args['<bundle_id>']
    #         print(args)
    #         # Loop over bundles
    #         logging.info("Analysis ID : {}".format(bundle))
    #         retcode = command(deepcopy(args)).run()
            
    #         # If any execution fails, then exit
    #         if retcode != 0:
    #             sys.exit(retcode)
    #         sys.exit(0)
    pass

@click.argument('out_dir')
@click.argument('analysis_id')
@click.option('--install-dir', help='optional directory to cache input datasets')
@click.option('--neurovault', default='group', help='neurovault upload mode (disable, all or group)')
@click.option('--force-upload', default=False, is_flag=True, help='neurovault upload mode (disable, all or group)')
@click.argument('fitlins_args', nargs=-1, type=click.UNPROCESSED)
@main.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_interspersed_args=False
))
def run(analysis_id, out_dir, install_dir, neurovault, force_upload, fitlins_args):
    print(install_dir)
    print(neurovault)
    print(force_upload)
    print(fitlins_args)
    click.echo('Initialized the database')

@main.command()
def install():
    click.echo('Dropped the database')
    
@main.command()
def upload():
    click.echo('Initialized the database')
