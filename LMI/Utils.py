import timeit


def check_int(s):
    if s.count(".") == 1:
        if not (s.split(".")[1].count("0") == len(s.split(".")[1])):
            return False
        return check_int_quick(s.split(".")[0])
    if s.count(".") > 1:
        return False
    return check_int_quick(s)


def check_int_quick(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


class RunTimeReturn:
    runReturnTemplate = """def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
"""

    def __init__(self):
        self.oldTemplate = None

    def __enter__(self):
        self.oldTemplate = timeit.template
        timeit.template = RunTimeReturn.runReturnTemplate
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        timeit.template = self.oldTemplate

    @staticmethod
    def run(function, number=1):
        return timeit.timeit(function, number=number)
