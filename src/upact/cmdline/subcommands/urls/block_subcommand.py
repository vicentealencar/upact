class BlockSubcommand(object):
    @staticmethod
    def kwargs():
        return ['urls_to_block', 'playtime_days', 'playtime_hours']

    def __init__(self, urls_to_block, playtime_days, playtime_hours):
        self.urls_to_block = urls_to_block
        self.playtime_days = playtime_days
        self.playtime_hours = playtime_hours
        self.result = None

    def _render(self):
        print("hello world!!")

    def __call__(self):
        self._render()
