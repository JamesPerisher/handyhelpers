import threading
import ctypes
import time



class ThreadExit(Exception):
    pass

class ThreadExitFailure(Exception):
    pass


class KillableThread(threading.Thread):
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type=None, value=None, traceback=None):
        self.end(type, value, traceback)
        return self

    def end(self, type, value, traceback):
        pass

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def kill(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            raise ThreadExitFailure('Failed to raise exception in thread %s can not kill execution.'%thread_id)
        return self.__exit__()


class TimeLoopedThread(KillableThread):
    def __init__(self, time=10, target=None, args=()):
        super().__init__()
        self.time = time
        self.target = target
        self.args = args

    def run(self, n):
        if self.target: self.target(n, *self.args)
         # override this function when class is inherited

    def _run(self):
        n = 0
        while True:
            self.runloop(n)
            n += 1
            time.sleep(self.time)

    def start(self):
        self.runloop = self.run
        self.run = self._run
        super().start()



class TimeoutThread(KillableThread):
    def __init__(self, timeout=1):
        super().__init__()
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, type=None, value=None, traceback=None):
        if type == ThreadExit : return True
        super().__exit__()

    def start(self):
        self.thread_id = threading.current_thread().ident
        print(dir(self.thread_id))
        print(self.thread_id)
        super().start()
        return self

    def run(self):
        time.sleep(self.timeout)

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, ctypes.py_object(ThreadExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, 0)
            raise ThreadExitFailure('Failed to raise exception in thread %s can not kill execution.'%self.thread_id)





with limmitedthread(1).start() as a:
    print(a)
    while True:
        print("a")
        time.sleep(0.1)

print("exited fine")
