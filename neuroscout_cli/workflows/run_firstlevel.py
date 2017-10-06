from neuroscout_cli.commands.install import Install
from neuroscout_cli.workflows.first_level import create_first_level

import json
import os
import tempfile
import pandas as pd


class FirstLevel(object):
    """ Validates arguments, and connect inputs to first level workflow"""
    def __init__(self, args):
        self.args = {}
        self.validate_arguments(args)
        self.create_workflow()

    def create_workflow(self):
        self.wf = create_first_level(**self.args)

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

        for directory in ['<out_dir>', '-w']:
            if args[directory] is not None:
                args[directory] = os.path.abspath(args[directory])
                if not os.path.exists(args[directory]):
                    os.makedirs(args[directory])

        self.args['work_dir'] = args['-w'] if args['-w'] else tempfile.mkdtemp()
        self.args['out_dir'] = args['<out_dir>']

        self.jobs = int(args.pop('--jobs'))

        # Install the needed inputs
        install_command = Install({'bundle': False,
                                   'data': False,
                                   '-i': self.args['-i'],
                                   '<bundle_id>': self.args['<bundle_id']})
        bids_dir = install_command.run()


        """ Process bundle arguments """
        ### TODO: get from bundle file
        bundle = args.pop('<bundle>')
        if not isinstance(bundle, dict):
            bundle = json.load(open(bundle, 'r'))
        self.args['subjects'] = list(pd.DataFrame(
            bundle['runs']).subject.unique())
        self.args['config'] = bundle['config']
        self.args['contrasts'] = bundle['contrasts']
        self.args['task'] = bundle['task_name']
        self.args['TR'] = bundle['TR']
        self.args['runs'] = bundle['runs']
        self.args['bids_dir'] = bids_dir
        # For now ignoring name and hash_id

        """ Write out design matrix """
        ### TODO: NEED TO EDIT THIS TO NEW BUNDLE
        pes = pd.DataFrame(bundle.pop('predictor_events')).rename(
            columns={'predictor_id': 'trial_type'})

        out_path = os.path.join(self.args['work_dir'], 'events')
        if not os.path.exists(out_path):
            os.mkdir(out_path)

        for r in bundle['runs']:
            # Write out event files for each run_id
            run_events = pes[pes.run_id == r['id']].drop('run_id', axis=1)
            ses = 'ses-{}_'.format(r['session']) if r['session'] else ''

            events_fname = os.path.join(out_path,
                                        'sub-{}_{}task-{}_run-{}_events.tsv'.format(
                r['subject'], ses, bundle['task_name'], r['number']))

            run_events.to_csv(events_fname, sep='\t', index=False)
