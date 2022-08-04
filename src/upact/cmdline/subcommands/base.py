class BaseSubcommand(object):
    def _render(self):
        raise NotImplementedError()

    def __call__(self):
        raise NotImplementedError()
