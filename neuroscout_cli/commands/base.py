"""The base command."""

from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):

    ''' A base command'''

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    def run(self):
        pass
