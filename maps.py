


class Map2D(object): # stores a 2D array of objects in an optimized 1D array
    def __init__(self, width, height, defaultfactory=lambda x,y: None):
        self.width = width
        self.height = height
        self.items = [None] * (self.width * self.height)

        for i,j in self: # fills the aray with an initialiser
            self[i] = defaultfactory(*i)

    def __repr__(self):
        return "{}(width={}, height={})".format(self.__class__.__name__, self.width, self.height)

    def __iter__(self):
        for i,j in enumerate(self.items):
            yield (i%self.width, i//self.width), j

    def getkey(self, key): # convert 2D key or 1D key into 1D key
        try:
            x, y = key
            return y*self.width + x
        except (TypeError, ValueError):
            return key

    def __getitem__(self, key:int):
        try:
            return self.items[self.getkey(key)]
        except IndexError:
            raise IndexError("{} index out of range".format(self.__class__.__name__))

    def __setitem__(self, key:int, value):
        self.items[self.getkey(key)] = value


class DirectionTile(object):
    def __init__(self, x=None, y=None):
        self.N = None
        self.NE = None
        self.E = None
        self.SE = None
        self.S = None
        self.SW = None
        self.W = None
        self.NW = None


        self.x = x
        self.y = y

    def _iterable(self):
        yield self.N
        yield self.NE
        yield self.E
        yield self.SE
        yield self.S
        yield self.SW
        yield self.W
        yield self.NW
    
    def __iter__(self):
        for i in self._iterable():
            if i != None:
                yield i


    def __repr__(self):
        return "{}(x={}, y={})".format(self.__class__.__name__, self.x, self.y)


class DirectionMap2D(Map2D): # stores a 2d array of DirectionTile decenndent objects
    def __init__(self, width, height, directiontileclass=DirectionTile):
        self.directiontileclass = directiontileclass
        super().__init__(width, height, self._maketile)

    def _maketile(self, x, y): # makes and assigns diretions to tiles
        current = self.directiontileclass(x, y)
        if x-1 >= 0:
            current.W = self[x-1, y]
            self[x-1, y].E = current

        if y-1 >= 0:
            current.N = self[x, y-1]
            self[x, y-1].S = current

        if x-1 >= 0 and y-1 >= 0:
            current.NW = current.N.W
            current.N.W.SE = current
        
        if x+1 < self.width and y-1 >= 0:
            current.NE = current.N.E
            current.N.E.SW = current


        return current
