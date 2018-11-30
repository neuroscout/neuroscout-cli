from neuroscout_cli.commands.base import Command
from datalad.api import install, get, unlock
from pathlib import Path
from shutil import copy
import requests
import json
import tarfile
import logging
from tqdm import tqdm

logging.getLogger().setLevel(logging.INFO)


def download_file(url, path):
    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)

    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    with open(path, 'wb') as f:
        with tqdm(total=total_size, unit='B',
                  unit_scale=True, unit_divisor=1024) as pbar:
            for data in r.iter_content(32*1024):
                f.write(data)
                pbar.update(len(data))


class Install(Command):

    ''' Command for retrieving neuroscout bundles and their corresponding
    data. '''
    def download_bundle(self):
        if not self.bundle_cache.exists():
            logging.info("Downloading bundle...")
            self.api.analyses.bundle(self.bundle_id, self.bundle_cache)

        tf = tarfile.open(self.bundle_cache)
        self.resources = json.loads(
            tf.extractfile('resources.json').read().decode("utf-8"))

        self.dataset_dir = self.install_dir / self.resources['dataset_name']
        self.bundle_dir = self.dataset_dir / 'derivatives' / 'neuroscout' / self.bundle_id

        # Probably need to add option to force-redownload
        if not self.bundle_dir.exists():
            self.bundle_dir.mkdir(parents=True, exist_ok=True)
            tf.extractall(self.bundle_dir)
            logging.info(
                "Bundle installed at {}".format(self.bundle_dir.absolute()))
            # Copy meta-data to root of dataset_dir
            copy(list(self.bundle_dir.glob('task-*json'))[0], self.dataset_dir)

        return self.bundle_dir.absolute()

    def download_data(self):
        self.download_bundle()

        remote_files = self.resources['func_paths'] + self.resources['mask_paths']
        remote_path = self.resources['preproc_address']

        preproc_dir = Path(self.dataset_dir) / 'derivatives' / 'fmriprep'

        try:
            if not preproc_dir.exists():
                # Use datalad to install the raw BIDS dataset
                install(source=remote_path,
                        path=str(preproc_dir))
            if (preproc_dir / 'fmriprep').exists():
                paths = [str(preproc_dir / 'fmriprep' / f) for f in remote_files]
                get(paths)
                get(str(preproc_dir / 'dataset_description.json'))
                if self.options.pop('--unlock', False):
                    unlock(paths)
        except Exception as e:
            message = e.failed[0]['message']
            if 'Failed to clone data from any candidate' not in message[0]:
                raise ValueError("Datalad failed. Reason: {}".format(message))

            logging.info("Attempting HTTP download...")
            for i, resource in enumerate(remote_files):
                filename = preproc_dir / resource
                logging.info("{}/{}: {}".format(i+1, len(remote_files), resource))

                if not filename.exists():
                    filename.parents[0].mkdir(exist_ok=True, parents=True)
                    download_file(remote_path + '/' + resource, filename)

        desc = {'Name': self.dataset_dir.parts[0], 'BIDSVersion': '1.0'}

        with (self.dataset_dir / 'dataset_description.json').open('w') as f:
            json.dump(desc, f)

        return self.bundle_dir.absolute()

    def run(self):
        self.bundle_cache = (self.home / self.bundle_id).with_suffix(".tar.gz")
        self.install_dir = Path(self.options.pop('--install-dir'))

        if self.options.pop('--no-download', False):
            return self.download_bundle()
        elif self.options.get('--dataset-name', False):
            self.dataset_dir = self.install_dir / self.options.pop('--dataset-name')
            self.bundle_dir = self.dataset_dir / 'derivatives' / 'neuroscout' / self.bundle_id
            if self.bundle_dir.exists():
                return self.bundle_dir.absolute()
            else:
                raise ValueError(
                    "Manually specified dataset directory does not contain",
                    "analysis bundle. Try again, or re-download bundle.")
        else:
            return self.download_data()
