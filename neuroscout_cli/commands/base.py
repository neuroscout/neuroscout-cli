"""The base command."""

from abc import ABCMeta, abstractmethod
from pathlib import Path
from pyns import Neuroscout
from ..tools.convert import check_convert_model

class Command(metaclass=ABCMeta):

    ''' A base command'''

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.bundle_id = self.options['<bundle_id>']
        self.args = args
        self.kwargs = kwargs
        self.api = Neuroscout()
        self.main_dir = Path(self.options.pop('<outdir>')) / f'neuroscout-{self.bundle_id}'
        self.bundle_dir = (self.main_dir / 'sourcedata' / 'bundle').absolute()
        
        self.model_path = check_convert_model(
            (self.bundle_dir / 'model.json').absolute()         
            ) # Convert if necessary

    @abstractmethod
    def run(self):
        pass
