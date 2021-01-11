import colorama
import datetime
from colorama import Fore, Back, Style
colorama.init()


class Input:
    def __init__(self, parent=None):
        self.parent = parent

    def raw(self):
        return input()

    def custom(self, *args):
        self.parent.custom(*args, end="")
        return self.raw()

    def log(self, *args):
        self.parent.log(*args, end="")
        return self.raw()

    def info(self, *args):
        self.parent.info(*args, end="")
        return self.raw()

    def warn(self, *args):
        self.parent.warn(*args, end="")
        return self.raw()

    def error(self, *args):
        self.parent.log(*args, end="")
        return self.error()

    def password(self, *args):
        self.parent.password(*args, end="")
        return self.raw()

    def success(self, *args):
        self.parent.success(*args, end="")
        return self.raw()


class Console:
    LOG =      Style.NORMAL + Back.BLACK + Fore.WHITE
    INFO =     Style.NORMAL + Back.BLACK + Fore.CYAN
    WARN =     Style.NORMAL + Back.BLACK + Fore.YELLOW
    ERROR =    Style.NORMAL + Back.BLACK + Fore.RED
    PASSWORD = Style.NORMAL + Back.BLUE + Fore.BLUE
    SUCCESS =  Style.NORMAL + Back.BLACK + Fore.GREEN

    def __init__(self, *args, show_level=True, date_format="%d/%m/%Y %H:%M:%S"):
        self.show_level = show_level
        self.date_format = date_format
        self.prefixes = args

        self.input = Input(self)

    def __repr__(self):
        return datetime.datetime.now().strftime(self.date_format) + " " + " ".join(self.prefixes)

    def print(*args, **kwargs):
        print(*args, **kwargs)

    def join(split, items):
        return str(split).join([str(x) for x in items])

    def level(args, level):
        if isinstance((args + ("",))[0], console) and args[0].show_level:
            return "[%s] "%level.upper()
        return ""

    def custom(*args, end="\n"):
        console.print(console.join("", args), end=end)

    def log(*args, end="\n"):
        console.custom(console.LOG,      console.level(args, "log"), console.join(" ", args), end=end)

    def info(*args, end="\n"):
        console.custom(console.INFO,     console.level(args, "info"), console.join(" ", args), end=end)

    def warn(*args, end="\n"):
        console.custom(console.WARN,     console.level(args, "warn"), console.join(" ", args), end=end)

    def error(*args, end="\n"):
        console.custom(console.ERROR,    console.level(args, "error"), console.join(" ", args), end=end)

    def password(*args, end="\n"):
        console.custom(console.PASSWORD, console.level(args, "password"), console.join(" ", args), end=end)

    def success(*args, end="\n"):
        console.custom(console.SUCCESS,  console.level(args, "success"), console.join(" ", args), end=end)

Console.input = Input(Console)
