from neuroscout_cli.commands.run import Run


class Upload(Run):
    ''' Command for running neuroscout workflows. '''

    def run(self):
        return super().run(upload_only=True)
