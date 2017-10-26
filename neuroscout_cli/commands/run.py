from neuroscout_cli.commands.base import Command
from neuroscout_cli.workflows.analysis import FirstLevel, GroupLevel


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
            first_runner = FirstLevel(self.options)
            first_lvdir = first_runner.args['out_dir']
            first_runner.execute()
            self.options['-f'] = first_lvdir
            group_runner = GroupLevel(self.options)
            group_runner.execute()
