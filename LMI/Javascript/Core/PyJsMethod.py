from js2py.pyjs import PyJsFunction, PyJsArguments, Js, undefined, MakeError


class PyJsMethod(PyJsFunction):
    def __init__(self, func, boundObj, **kwargs):
        super().__init__(func, **kwargs)
        self.boundObj = boundObj

    def call(self, this, args=()):
        """Calls this function and returns a result
        (converted to PyJs type so func can return python types)

        this must be a PyJs object and args must be a python tuple of PyJs objects.

        arguments object is passed automatically and will be equal to Js(args)
        (tuple converted to arguments object).You dont need to worry about number
        of arguments you provide if you supply less then missing ones will be set
        to undefined (but not present in arguments object).
        And if you supply too much then excess will not be passed
        (but they will be present in arguments object).
        """
        if not hasattr(args, '__iter__'):  # get rid of it later
            args = (args,)
        args = tuple(Js(e) for e in args)  # this wont be needed later

        arguments = PyJsArguments(
            args, self)  # tuple will be converted to arguments object.
        argLen = self.argcount - 1  # function expects this number of args.
        if len(args) > argLen:
            args = args[0:argLen]
        elif len(args) < argLen:
            args += (undefined,) * (argLen - len(args))
        args += this, arguments  # append extra params to the arg list
        try:
            return Js(self.code(self.boundObj, *args))
        except NotImplementedError:
            raise
        except RuntimeError as e:  # maximum recursion
            try:
                msg = e.message
            except Exception as se:
                _ = se
                msg = repr(e)
            raise MakeError('RangeError', msg)
