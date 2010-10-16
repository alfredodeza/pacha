class MockSys(object):
    """Can grab messages sent to stdout or stderr"""
    def __init__(self):
        self.message = []

    def __call__(self, *args, **kw):
        pass

    def write(self, string):
        self.message.append(string)
        pass

    def captured(self):
        return ''.join(self.message)

