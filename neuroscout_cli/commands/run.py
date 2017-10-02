from neuroscout_cli.commands.base import Command
from neuroscout_cli.workflows import run_firstlevel
from neuroscout_cli.workflows import run_group


class Run(Command):
    def run(self):
        first = self.options.pop('first_level')
        group = self.options.pop('group')
        if first:
            runner = run_firstlevel.FirstLevel(self.options)
            runner.execute()
        elif group:
            runner = run_group.GroupLevel(self.options)
            runner.execute()
