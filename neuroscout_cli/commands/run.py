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
            self.options = run_group.validate_arguments(self.options)
            run = self.options.pop('run')
            jobs = int(self.options.pop('--jobs'))
            wf = run_group.group_onesample(**self.options)

            if run:
                if jobs == 1:
                    wf.run()
                else:
                    wf.run(plugin='MultiProc', plugin_args={'n_procs': jobs})
            else:
                wf
