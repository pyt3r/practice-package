class DriverFactory:

    _modes = {
        'basic': 'basic',
        'leet': 'leet,'
    }

    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        meth = getattr(self, self.name)
        return meth(*args, **kwargs)

    @staticmethod
    def basic(Solution, method):
        from practice.util.driver import Driver
        return Driver(Solution, method)

    @staticmethod
    def leet(text):
        raise NotImplementedError
