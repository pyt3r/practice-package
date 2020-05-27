class Driver:

    def __init__(self, solution, method):
        self.solution = solution
        self.method = method

    def run(self, **inputs):
        fun = getattr(self.solution, self.method)
        printMe = [
            ('function', fun),
            ('inputs', inputs), ]
        Driver.print(printMe)
        outputs = fun(**inputs)
        Driver.print([('outputs', outputs), ])
        return outputs

    @staticmethod
    def print(printMe):
        from pprint import pprint as pp

        for banner, obj in printMe:
            print(Driver.banner(banner))
            pp(obj)

    @staticmethod
    def banner(x):
        return '\n' + (' {} '.format(x).center(50, "="))
