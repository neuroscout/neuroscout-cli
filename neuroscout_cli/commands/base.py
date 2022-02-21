"""The base command."""

import logging
from abc import ABCMeta, abstractmethod
from pathlib import Path
from pyns import Neuroscout
from ..tools.convert import check_convert_model

class Command(metaclass=ABCMeta):

    ''' A base command'''

    def __init__(self, options):
        self.options = options
        self.bundle_id = self.options['analysis_id']
        self.api = Neuroscout()
        self.main_dir = Path(self.options['out_dir']) / f'neuroscout-{self.bundle_id}'
        self.bundle_dir = (self.main_dir / 'sourcedata' / 'bundle').absolute()
        logging.info("Analysis ID : {}".format(self.bundle_id))

        self.model_path = (self.bundle_dir / 'model.json').absolute()
        
        # Convert model to v1 if necessary
        if self.model_path.exists():
            self.model_path = check_convert_model(
                (self.bundle_dir / 'model.json').absolute()         
                ) 

    @abstractmethod
    def run(self):
        pass
