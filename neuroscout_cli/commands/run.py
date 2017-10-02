from neuroscout_cli.commands.base import Command
from neuroscout_cli.workflows import fmri_bids_firstlevel as first_level
from neuroscout_cli.workflows import fmri_group as group_level


class Run(Command):
    def run(self):
        first = self.options.pop('first_level')
        group = self.options.pop('group')
        if first:
            runner = first_level.FirstLevel(self.options)
            runner.execute()
        elif group:
            self.options = group_level.validate_arguments(self.options)
            run = self.options.pop('run')
            self.options.pop('make')
            jobs = int(self.options.pop('--jobs'))
            wf = group_level.group_onesample(**self.options)

            if run:
                if jobs == 1:
                    wf.run()
                else:
                    wf.run(plugin='MultiProc', plugin_args={'n_procs': jobs})
            else:
                wf
