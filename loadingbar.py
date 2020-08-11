import time

class LoadingBar:
    def __init__(self, items=100, speed=0, width=30, speed_units="kb", averge_len=10):
        self.timestart = time.time()
        self.elapsedtime = 0
        self.completed = 0
        self.items = items
        self.speed = speed
        self.width = width
        self.percent = 0

        self.speeds = list()
        self.speed_units = speed_units
        self.averge_len = averge_len

    def update(self, items, speed):
        self.speeds.append(speed)
        if not len(self.speeds) < self.averge_len : self.speeds.pop(0)
        self.completed = items
        self.speed = speed
        self.percent = self.completed / self.items
        self.percent = round(self.completed/self.items, 2)
        self.elapsedtime = round(time.time() - self.timestart, 2)
        return self

    def complete(self):
        self.update(self.items, self.speeds[-1])
        return self


    def print(self, start="    "):
        solidp = round(self.percent*100)
        full = round(self.width *self.percent)
        average_speed = round(sum(self.speeds)/len(self.speeds), 2)
        units = " %s/s"%self.speed_units

        line = "%s|%s%s|   %s/%s [%06s%%] in %04ss (%04s%s) average %06s%s%s"%(start, "█"*full, " "*(self.width-full), self.completed, self.items, round(self.percent*100, 2), self.elapsedtime, self.speed, units,average_speed, units," "*10)

        print(line, end="\r")
        return self
