from hashlib import md5
import logging
import base64


h = logging.StreamHandler()
serial_log = logging.Logger(__name__)

h.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
serial_log.addHandler(h)

serial_log.critical("""
# NOTE: This program serialises objects that if saved to an external source can be directly modified by the end user this may result in a security risk if
#       1) Any serialisable object has any functionality the end user should not be allowed to access
#       2) Any data that is deserialised is passed to any sensitive function i.e. ('exec', 'eval', 'os.system', etc), (NOTE: Doing so is NEVER a good idea)
""")
serial_log.setLevel(logging.ERROR)

# for global class_space for root serialisation
global class_space
class_space = dict()

# ====================== SERIAL OBJECTS AND BASIC CONVERSION ======================

class SerialTracker:
    def __init__(self, cls) -> None:
        self.self = self.cls = cls

    def __repr__(self) -> str:
        return "SerialTracker(%s)"%self.cls.__repr__()

    def __setattr__(self, key, value):
        try:
            if self.cls: pass
            self.cls.trackedobjects.append(key)
            self.cls.__setattr__(key, value)
        except AttributeError as e:
            super().__setattr__(key, value)


class NonSerial:
    def __repr__(self) -> str:
        return "NonSerial()"

class SerialManager:
    def __init__(self, name):
        self.name = name
        self.class_space = dict()
    
    def _warn(self, obj):
        pass

    def Serialiser(mself, *args, **kwargs):
        mself._warn(args[0])
        return _Serialiser(mself, *args, **kwargs)

    def Constructor(mself, *args, **kwargs):
        mself._warn(args[0])
        return _Constructor(mself, *args, **kwargs)


class _Serialiser:
    def __init__(self, master, obj) -> None:
        self.master = master
        self.objtable = dict()
        self.obj = obj

    def __repr__(self) -> str:
        return "%s(%s)"%(self.__class__.__name__, str(self.obj))

    def get(self):
        return {"object_tabel":self.objtable, "data":self._serialise(self.obj)} # seems that self.objtable is returned with evaluated results from self._serialise(

    def _serialise(self, obj):
        if type(obj) in (type(x) for x in [NonSerial(), str(), int(), float(), complex(), bytes(), list(), dict()]):
            lookup = {
                type(NonSerial()) : ("nos", self._serialise_nonserial),
                type(bool())      : ("bol", self._serialise_bool     ),
                type(int())       : ("int", self._serialise_int      ),
                type(float())     : ("flt", self._serialise_float    ),
                type(complex())   : ("cpx", self._serialise_complex  ),
                type(str())       : ("str", self._serialise_str      ),
                type(bytes())     : ("byt", self._serialise_bytes    ),
                type(list())      : ("lst", self._serialise_list     ),
                type(dict())      : ("dic", self._serialise_dict     )
            }[type(obj)]
            return {"type": lookup[0], "data": lookup[1](obj)}
        try:
            if not obj._serialisable: return self._serialise(NonSerial())
        except AttributeError:
            return self._serialise(NonSerial())

        if obj._linkedserialisable: # pretty sure this can't ever reach state to raise exception
            has = obj.gethash()
            if not has in self.objtable:
                self.objtable[has] = "TMP"
                self.objtable[has] = obj.serialise(self)
            return {"type": "lnk", "data": has}

    def _serialise_nonserial(self, obj):
        return "NoSerial"

    def _serialise_bool(self, obj):
        return obj

    def _serialise_int(self, obj):
        return obj

    def _serialise_float(self, obj):
        return obj

    def _serialise_complex(self, obj):
        return [obj.real, obj.imag]

    def _serialise_str(self, obj):
        return base64.b64encode(obj.encode()).decode()

    def _serialise_bytes(self, obj):
        return base64.b64encode(obj).decode()

    def _serialise_list(self, obj):
        return [self._serialise(x) for x in obj]

    def _serialise_dict(self, obj):
        return [[self._serialise(x), self._serialise(obj[x])] for x in obj]



class _Constructor:
    def __init__(self, master, data) -> None:
        self.master = master
        self.objtable = data["object_tabel"]
        self.data = data["data"]

    def get(self):
        for i in self.objtable:
            self.objtable[i] = self._construct(self.objtable[i]) # reconstructs the obj table

        for i in self.objtable:
            for j in self.objtable[i].trackedobjects:
                try:
                    objdata = self.objtable[i].__getattribute__(j)
                    if objdata["type"] == "lnk":
                        constructedlnk = self._construct_link(objdata)
                        self.objtable[i].__setattr__(j, constructedlnk)
                    else:
                        self.objtable[i].__setattr__(j, self._construct(objdata))
                except (KeyError, AttributeError):
                    continue

        return self._construct(self.data, _flink=True) # efficiency of O(2n)


    def _construct_link(self, obj):
        return self.objtable[obj["data"]]

    def _construct_nonserial(self, obj):
        return NonSerial()

    def _construct_bool(self, obj):
        return obj

    def _construct_int(self, obj):
        return obj

    def _construct_float(self, obj):
        return obj

    def _construct_complex(self, obj):
        return complex(obj[0], obj[1])

    def _construct_str(self, obj):
        return base64.b64decode(obj.encode()).decode()

    def _construct_bytes(self, obj):
        return base64.b64decode(obj.encode())

    def _construct_list(self, obj):
        return [self._construct(x) for x in obj]

    def _construct_dict(self, obj):
        return {self._construct(x[0]) : self._construct(x[1]) for x in obj}

    def _construct(self, obj, _flink=False):
        if _flink:
            if obj["type"] == "lnk":
                return self._construct_link(obj)
        if obj["type"] in ("nos", "bol", "int", "flt", "cpx", "str", "byt", "lst", "dic"):
            return {
                "nos" : self._construct_nonserial,
                "bol" : self._construct_bool,
                "int" : self._construct_int,
                "flt" : self._construct_float,
                "cpx" : self._construct_complex,
                "str" : self._construct_str,
                "byt" : self._construct_bytes,
                "lst" : self._construct_list,
                "dic" : self._construct_dict
            }[obj["type"]](obj["data"])
        else:
            try:
                typ = self.master.class_space[obj["type"]]
            except KeyError:
                raise AttributeError("Can't access type '{}' from '{}' context.".format(obj["type"], self.master))
            else:
                newobj = typ(*self._construct(obj["encoding"]["args"]), **self._construct(obj["encoding"]["kwargs"]))

                for i in obj["data"]:
                    newobj.__setattr__(i, obj["data"][i])
                return newobj


# ====================== MAIN SERIAL FUNCTIONALITY ======================

class SerialManager(SerialManager):

    def serialisable(mself, *default_args, **default_kwargs):
        def func(mclass):
            class Serialisable(mclass):
                mself._warn(mclass)
                def __init__(self, *args, **kwargs) -> None:
                    self._serialisable = True
                    serf = SerialTracker(self)
                    self.trackedobjects = list()
                    super().__init__(serf, *args, **kwargs)

                def __repr__(self) -> str:
                    return "<Serialisable(%s)>"%super().__repr__()

                def gethash(self):
                    strval = ":|:".join([mclass.__name__] + self.trackedobjects)
                    return md5(strval.encode()).hexdigest()

                def serialise(self, serialiser):
                    out = dict()
                    for i in self.trackedobjects:
                        out[i] = serialiser._serialise(self.__dict__[i])
                    return {"type": mclass.__name__, "encoding":{"args":serialiser._serialise(list(default_args)), "kwargs":serialiser._serialise(dict(default_kwargs))}, "data": out}

            mself.class_space[mclass.__name__] = Serialisable
            return Serialisable
        return func

    def linkedserialisable(mself, *default_args, hash=None, **default_kwargs):
        def func(mclass):
            class LinkedSerialisable(mself.serialisable(*default_args, **default_kwargs)(mclass)):
                mself._warn(mself)
                def __init__(self, *args, **kwargs) -> None:
                    super().__init__(*args, **kwargs)
                    self._linkedserialisable = True

                def __repr__(self) -> str:
                    return "<LinkedSerialisable(%s)>"%super().__repr__()

            mself.class_space[mclass.__name__] = LinkedSerialisable
            return LinkedSerialisable
        return func


class RootSerialManager(SerialManager):
    def __init__(self):
        global class_space
        super().__init__("root:%s"%__name__)
        self.class_space = class_space

    def _warn(self, obj):
        if type(obj) != type(self):
            serial_log.warning("[{}] Using root SerialManager for object '{}'.".format(self.name, str(obj)))

sm = RootSerialManager() # access though to the global class_space
serialisable = sm.serialisable
linkedserialisable = sm.linkedserialisable

Serialiser  = sm.Serialiser
Constructor = sm.Constructor

