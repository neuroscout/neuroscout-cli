from neuroscout_cli.commands.base import Command
from neuroscout_cli.workflows.run_firstlevel import FirstLevel
from neuroscout_cli.workflows.run_grouplevel import GroupLevel


class Run(Command):

    ''' Command for running neuroscout workflows. '''

    def run(self):
        first = self.options.pop('first_level')
        group = self.options.pop('group_level')
        if first:
            runner = FirstLevel(self.options)
            runner.execute()
        elif group:
            runner = GroupLevel(self.options)
            runner.execute()
        else:
            # TODO: chain first level and group level
            pass
