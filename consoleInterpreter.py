from exceptions import *

class Interpreter:
    @staticmethod
    def isValid(typee, content):
        if isinstance(content, type(None)): return True
        try:
            typee(content)
            return True
        except ValueError:
            return False

    @staticmethod
    def argParser(content):
        content = content + " "
        double = False
        single = False
        last = 0
        out = []
        for i,j in enumerate(content):

            # check if in quotes
            if j == "\"":
                if not single:
                    double = not double
            if j == "'":
                if not double:
                    single = not single
            if single or double:
                continue

            # split into args
            if j.strip() == "":
                arg = content[last:i].strip()
                if arg[0] in ["\"", "'"]:
                    arg = arg[1:-1]
                out.append(arg)
                last = i
        if content[last::].strip() != "":
            raise SyntaxError("Unclosed arguments")

        return out


    @staticmethod
    def convert(typee, content):
        if isinstance(content, type(None)): return None
        return typee(content)



class Arg:
    def __init__(self, expected, desc, optional=False, multi=False):
        self.expected = expected
        self.desc     = desc
        self.optional = optional
        self.multi = multi

    def __repr__(self):
        return "arg_%s%s%s"%(self.expected, "_" if self.optional else "*", "+" if self.multi else "-")


    def check(self, data):
        return Interpreter.isValid(self.expected, data)



class Command(list):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name if type(name) == type(list()) else [name]

    def __repr__(self):
        return "command%s(%s)"%(self.name,super().__repr__())

    def __setitem__(self, index, value):
        if not isinstance(value, Arg) : raise InvalidCommandArgError("Command can only contain arguments.")
        super().__setitem__(index, value)

    def append(self, value):
        if not isinstance(value, Arg) : raise InvalidCommandArgError("Command can only contain arguments.")
        super().append(value)

    def add_arg(self, expected=str, description="Argument description.", optional=False):
        self.append(Arg(expected, description, optional))

    def check(self, args):
        return (args[0] in self.name)

    def execute(self, args, *aargs, **kwargs):
        args = args[1::]

        required = len(args)
        if len([0 for x in self if not x.optional]) > required : raise NotEnoughArgumentsError("Too many argument for '%s'."%self)

        args = args + [None]*(len(self)-required)

        out = []
        i = 0
        for j in args:
            if len(self) <= i : raise TooManyArgumentsError("Too many argument for '%s'."%self)
            if not self[i].check(j):
                if self[i].multi:
                    i += 1
                    out.append(self[i].expected(j))
                    continue
                raise InvalidArgumentError("The value '%s' does not match '%s'."%(j, self))
            out.append(Interpreter.convert(self[i].expected, j))

            if self[i].multi : continue
            i += 1


        return self.event(out, *aargs, **kwargs)

    def event(self, command_args, *args, **kwargs):
        # overwrite for command funtionality
        # default event using arguments of
        #    arguments form command line 'command_args'
        #    arguments forwarded form execute as args
        #    keywords forwarded from execute as 'kwargs'
        return True

    def setEvent(self, event):
        self.event = event


class CommandConsole(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "\n".join(["console("] + [str(x) for x in self] + [")"])

    def __setitem__(self, index, value):
        if not isinstance(value, Command) : raise InvalidCommandArgError("Command can only contain arguments.")
        super().__setitem__(index, value)

    def command(self, name, *args):
        def commandDecorator(func):
            new_command = Command(name)
            for i in args:
                new_command.append(i)
            new_command.setEvent(func)
            self.append(new_command)
            return func
        return commandDecorator


    def append(self, value):
        if not isinstance(value, Command) : raise InvalidCommandArgError("Command can only contain arguments.")
        super().append(value)

    def execute(self, line, *args, **kwargs):
        ag = Interpreter.argParser(line)
        exceptions = []
        for i in self:
            if i.check(ag):
                try:
                    return i.execute(ag, *args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
        if not len(exceptions) == 0 : raise MultipleExceptionsError(exceptions)
        raise MultipleExceptionsError([NoCommandError("No matching command for '%s'"%line)])

    def handleExecute(self, *args, **kwargs):
        try:
            return self.execute(*args, **kwargs)
        except MultipleExceptionsError as e:
            return e
