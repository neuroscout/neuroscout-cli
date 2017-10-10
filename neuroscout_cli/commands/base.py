"""The base command."""

from abc import ABCMeta, abstractmethod
from six import with_metaclass


class Command(with_metaclass(ABCMeta)):

    ''' A base command'''

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    def run(self):
        pass
