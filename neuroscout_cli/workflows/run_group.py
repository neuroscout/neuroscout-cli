from .group_level import create_group_level
import os


class GroupLevel(object):
    """ Validates arguments, and connect inputs to group level workflow"""
    def __init__(self, args):
        self.args = {}
        self.validate_arguments(args)
        self.create_workflow()

    def create_workflow(self):
        """
        Import model specific files
        """
        self.wf = create_group_level(**self.args)

    def execute(self):
        if self.run:
            if self.jobs == 1:
                self.wf.run()
            else:
                self.wf.run(plugin='MultiProc', plugin_args={'n_procs': self.jobs})
        else:
            return self.wf

    def validate_arguments(self, args):
        """ Validate and preload command line arguments """

        # Clean up names
        var_names = {'<firstlv_dir>': 'firstlv_dir',
                     '<output>': 'out_dir',
                     '-w': 'work_dir'}

        if args.pop('-c'):
            from nipype import config
            cfg = dict(logging=dict(workflow_level='DEBUG'),
                       execution={'stop_on_first_crash': True})
            config.update_config(cfg)

        for old, new in var_names.iteritems():
            args[new] = args.pop(old)

        self.jobs = int(args.pop('--jobs'))

        for directory in ['out_dir', 'work_dir']:
            if args[directory] is not None:
                args[directory] = os.path.abspath(args[directory])
                if not os.path.exists(args[directory]):
                    os.makedirs(args[directory])

        return args
