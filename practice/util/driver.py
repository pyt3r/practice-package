from pprint import pprint as pp


class Driver:

    banner = lambda x: '\n' + (' {} '.format(x).center(45, "="))

    def __init__(self, solution, method):
        self.solution = solution
        self.method = method

    def run(self, **inputs):

        fun = getattr(self.solution, self.method)
        outputs = fun(**inputs)

        printMe = [
            ('function', fun),
            ('inputs', inputs),
            ('outputs', outputs), ]

        for banner, o in printMe:
            print(Driver.banner(banner))
            pp(o)

        return outputs


