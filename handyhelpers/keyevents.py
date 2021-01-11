from pynput import keyboard
from pynput.keyboard import Key, KeyCode

from pynput import mouse

class Combination():
    def __init__(self, *args):
        self.sequence = list(x for x in args if isinstance(x, (keyboard.Key, keyboard.KeyCode)))

        self.__repr__ = lambda x : "Hello(coolio)"

    __ne__ = lambda self,other : not self.__eq__(other)
    __hash__ = lambda self : hash(tuple(self.sequence))
    __repr__ = lambda self : "Combination(%s)"%(", ".join([str(x) for x in self.sequence]))
    __getitem__ = lambda self,index : self.sequence[index]

    def __eq__(self, other):
        try:
            return self.sequence == other.sequence
        except:
            return False

    def add(self, other):
        if isinstance(other, (keyboard.Key, keyboard.KeyCode)) : self.sequence.append(other); return self
        raise TypeError("Invalid Key '%s'."%other)

    def get(self, index, default):
        try:
            return self.sequence[index]
        except IndexError:
            return default

    def clear(self):
        self.sequence = list()

    def serialise(self):
        return ", ".join(str(x) for x in self.sequence)


class Listener(keyboard.Listener):
    def __init__(self, *args, combinations=dict(), **kwargs):
        super().__init__(on_press=self.on_press, on_release=self.on_release)
        self.current = Combination()
        self.combinations = {Combination(): lambda key: "no op"}
        self.combinations.update(combinations)

    def on_mouse(self, x):
        print("mouse", x)

    def on_press(self, key):
        if self.current.get(-1, None) == key : return
        self.current.add(key)

        try:
            self.combinations[self.current](self.current)
        except KeyError as e:
            self.combinations[Combination()](self.current)

    def on_release(self, key):
        self.current.clear()

    def event(self, combination=None):
        combination = Combination() if combination == None else combination
        def call_fn(fn):
            self.combinations[combination] = fn
            return fn
        return call_fn
