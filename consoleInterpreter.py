class interpreter:
    def isValid(self, typee, content):
        try:
            typee(content)
            return True
        except ValueError:
            return False


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
