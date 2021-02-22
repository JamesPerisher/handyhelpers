import time
from .customthreading import KillableThread

class Context(object):
    def __init__(self) -> None:
        self.threads = list()

    def contextless(self, obj, _passback=None, _threaded=False): # escapes with context becouse
        if _threaded:
            with obj as contextobj:
                _passback.value = contextobj
                _passback.pause = False
                while True:
                    time.sleep(1)
        else:
            _passback = lambda x:x
            _passback.value = None
            _passback.pause = True
            current_thread = KillableThread(target=self.contextless, args=(obj, _passback, True), daemon=True)
            self.threads.append(current_thread)
            current_thread.start()

            while _passback.pause:
                time.sleep(1)
            return _passback.value

    def kill(self):
        for i in self.threads:
            i.kill()