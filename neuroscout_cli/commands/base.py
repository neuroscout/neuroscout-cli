"""The base command."""

from abc import ABCMeta, abstractmethod
from pathlib import Path
from pyns import Neuroscout


class Command(metaclass=ABCMeta):

    ''' A base command'''

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.bundle_id = self.options['<bundle_id>']
        self.args = args
        self.kwargs = kwargs
        self.home = Path.home() / '.neuroscout'
        self.home.mkdir(exist_ok=True)
        self.api = Neuroscout()

    @abstractmethod
    def run(self):

        pass
