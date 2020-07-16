from .customthreading import KillableThread
import sqlite3
import time


DELAY = 0.25

class EmptyPlacerholder():
    def __init__(self):
        pass


class DatabaseManager(KillableThread):

    def __init__(self, file=":memory:", timeout=10):
        super().__init__()
        self.file = file
        self.timeout = timeout # timeout in seconds

        self.command_stack = []
        self.outvalues = {}

        self.working = True
        self.doing = True

    def kill(self):
        self.working = False
        super().kill()

    def execute(self, command, timeout=-99999):
        timeout = self.timeout if timeout == -99999 else timeout
        temp_key = time.time()
        n = temp_key + self.timeout
        local_empty = EmptyPlacerholder()

        self.outvalues[temp_key] = local_empty
        self.command_stack.append((temp_key, command))


        while self.outvalues[temp_key] == local_empty: # waits till command executed
            if time.time() > n: # it took too long
                raise TimeoutError("Timed out while waiting for serialised database interaction.")

            time.sleep(DELAY)

        temp_out = self.outvalues[temp_key]
        self.outvalues.pop(temp_key) # clear value from dict

        return temp_out

    def commit(self):
        self.execute(":x:x:commit:x:x:")

    def run(self): # auto colled on Thread start
        # print("Started thread: %s"%str(self))
        self.conn = sqlite3.connect(self.file)
        self.crsr = self.conn.cursor()

        while self.working: # TODO: fix loop ineffeciencyies
            if len(self.command_stack) == 0:
                self.doing = False
            for i in self.command_stack:
                try:
                    current = self.command_stack.pop(0)
                    if current[1] == ":x:x:commit:x:x:":
                        self.outvalues[current[0]] = self.conn.commit()
                        # print("Commit to db")
                        continue

                    # print("{0: <12} {1} {2}".format("Running: ", current[0], current[1].replace("            ", " ").replace("\n", "\n       ")))

                    ee = None

                    try:
                        # print("SQL Command: %s" %current[1])
                        self.crsr.execute(current[1])
                    except Exception as e:
                        # print("before e.args")
                        # print(e.args)
                        if "UNIQUE constraint failed:" in e.args[0]:
                            log.error("{0: <12} {1}, {2}".format("Record not unique: ",str(e.args[0]), str(current[1])))
                        elif "FOREIGN KEY constraint failed" in e.args[0]:
                            log.error("{0: <12} {1}, {2}".format("participant or event does not exist: ",str(e.args[0]), str(current[1])))
                        else:
                            raise e

                    self.outvalues[current[0]] = self.crsr.fetchall()

                except Exception as e:
                    self.outvalues[current[0]] = e
                    raise e

            time.sleep(DELAY)
        # print("Killed:",  str(self))
