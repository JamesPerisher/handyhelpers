from exceptions import *

class interpreter:
    def argParser(self, content):
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



class arg:
    def __init__(self, expected, desc, optional, multi=False):
        self.expected = expected
        self.desc     = desc
        self.optional = optional
        self.multi = multi

    def __repr__(self):
        return "arg(expected='%s', desc='%s', optional='%s', multi='%s')"%(self.expected, self.desc, self.optional, self.multi)

    def isValid(self, typee, content):
        try:
            typee(content)
            return True
        except ValueError:
            return False

    def check(self, data):
        return self.isValid(self.expected, data)



class command:
    def __init__(self, name):
        self.name = name if type(name) == type(list()) else [name]
        self.args = []

    def __repr__(self):
        return "command(%s)"%self.args

    def append(self, expected=str, description="Argument description.", optinal=False):
        self.args.append(arg(expected, description, optinal))

    def check(self, args):
        return (args[0] in self.name)

    def execute(self, args, *aargs, **kwargs):
        args = args[1::]
        i = 0
        for j in args:
            if len(self.args) <= i : raise TooManyArguments("Too many argument for '%s'."%self)
            if not self.args[i].check(j):
                if self.args[i].multi:
                    i += 1
                    continue
                raise InvalidArgument("The value '%s' does not match '%s'."%(j, self))

            if self.args[i].multi : continue
            i += 1

        return self.event(args, *aargs, **kwargs)

    def event(self, command_args, *args, **kwargs):
        # overwrite for command funtionality
        # default event using arguments of
        #    arguments form command line 'command_args'
        #    arguments forwarded form execute as args
        #    keywords forwarded from execute as 'kwargs'
        return True





i = interpreter()
x = i.argParser("hello 'world hehe ee'")
print(x)


c = command("hello")
c.append()
print(c)

print(c.execute(x))
