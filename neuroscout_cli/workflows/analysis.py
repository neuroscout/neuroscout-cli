from neuroscout_cli.commands import Install
from neuroscout_cli.workflows.first_level import create_first_level
from neuroscout_cli.workflows.group_level import create_group_level

import json
import os
import tempfile
import pandas as pd

from abc import ABCMeta, abstractmethod
from os.path import join
from six import with_metaclass


class Level(with_metaclass(ABCMeta)):
    """ Validates arguments, and connect inputs to a workflow """
    def __init__(self, args):
        self.args = {}
        self.validate_arguments(args)
        self.create_workflow()

    @abstractmethod
    def create_workflow(self):
        pass

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
        if args.pop('-c'):
            from nipype import config
            cfg = dict(logging=dict(workflow_level='DEBUG'),
                       execution={'stop_on_first_crash': True})
            config.update_config(cfg)

        for directory in ['-o', '-w']:
            if args[directory] is not None:
                args[directory] = os.path.abspath(args[directory])
                if not os.path.exists(args[directory]):
                    os.makedirs(args[directory])

        self.args['work_dir'] = args['-w'] if args['-w'] else tempfile.mkdtemp()
        self.args['out_dir'] = args['-o'] if args['-o'] else os.getcwd()

        self.jobs = int(args.pop('--jobs'))
        self.run = True


class FirstLevel(Level):
    """ Validates and creates a first level workflow. """
    def create_workflow(self):
        self.wf = create_first_level(**self.args)

    def contrasts_bids_to_fsl(self, bids_contrasts):
        fsl_contrasts = []
        for bids_con in bids_contrasts:
            preds = [str(p['id']) for p in bids_con['predictors']]
            fsl_con = [bids_con['name'], bids_con['contrastType'], preds, bids_con['weights']]
            fsl_contrasts.append(fsl_con)
        return fsl_contrasts

    def validate_arguments(self, args):
        super(FirstLevel, self).validate_arguments(args)
        # Install the needed inputs
        install_command = Install({'bundle': False,
                                   'data': False,
                                   '-i': args['-i'],
                                   '<bundle_id>': args['<bundle_id>']})
        bundle_path, bids_dir = install_command.run()

        # Process analysis information
        with open(join(bundle_path, 'analysis.json'), 'r') as f:
            bundle = json.load(f)
        self.args['subjects'] = list(pd.DataFrame(
            bundle['runs']).subject.unique())
        self.args['config'] = bundle['config']
        self.args['contrasts'] = self.contrasts_bids_to_fsl(bundle['contrasts'])
        self.args['task'] = bundle['task_name']
        self.args['TR'] = bundle['TR']
        self.args['runs'] = bundle['runs']
        self.args['bids_dir'] = bids_dir
        # For now ignoring name and hash_id
        self.args['event_data'] = pd.DataFrame.from_csv(join(bundle_path, 'events.tsv'), sep='\t')


class GroupLevel(Level):
    """ Validates and creates a group level workflow. """
    def create_workflow(self):
        self.wf = create_group_level(**self.args)

    def validate_arguments(self, args):
        super(GroupLevel, self).validate_arguments(args)
        self.args['firstlv_dir'] = args.pop('<firstlv_dir>')
