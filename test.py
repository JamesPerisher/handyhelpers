from handyhelpers.escapecontext import Context
from handyhelpers import *
import logging

if __name__ == "__main__":

    print("[BEGIN] Testing escapecontext.py...")

    c = Context()
    aa = open("LICENSE")
    cf = c.contextless(aa)

    if not cf.readline() == "MIT License\n":
        print("[ERROR] In escapecontext.py")
    
    else:
        c.kill()
        print("[DONE] No Errors detected")


    print("[BEGIN] Testing virtualfilesystem.py...")
    vd = VirtualDrive(autoadd=True)
    open = vd.open
    openfile = vd.openfile
    open("V:/Users/Dave")
    open("V:/Users/Bob")
    with openfile("V:/Users/Dave/notes.txt") as f:
        f.write("filecontent\nfilecontent123")
    render = "\n".join(vd.render())
    # print(render)


    savestate = vd.save()

    vo = VirtualObject.fromsave(savestate)
    rendersaved = "\n".join(vo.render())
    if not (render == rendersaved):
        print("[ERROR] In virtualfilesystem.py")
    else:
        print("[DONE] No Errors detected")


    print("[BEGIN] Testing config.py...")
    c = Config.from_memory()
    savetxt = "Hello World!"
    c["test"] = savetxt
    c.save()
    # print(c.file.read()["test"] == savetxt)
    print("[DONE] No Errors detected")


    print("[BEGIN] Testing serialise.py...")
    print(serial_log)

    # using root serialisation context
    @linkedserialisable(0, 0)
    class test1:
        def __init__(self, serf, x, y) -> None:
            super().__init__()
            serf.x = x
            serf.y = y

    
    @linkedserialisable(5, 5)
    class test2:
        def __init__(self, serf, x, y) -> None:
            serf.x = x
            serf.y = y

    t1 = test1(10, 15)
    t2 = test2(t1, 20)
    t1.x = t2

    serilaised =  Serialiser(t1).get()
    deserialised = Constructor(serilaised).get()
    print("global context STATUS:", {True:"Good", False:"Bad"}[t1.x.y == deserialised.x.y])


    ssm = SerialManager(__name__)
    @ssm.linkedserialisable(0, 0)
    class test1:
        def __init__(self, serf, x, y) -> None:
            super().__init__()
            serf.x = x
            serf.y = y

    
    @ssm.linkedserialisable(5, 5)
    class test2:
        def __init__(self, serf, x, y) -> None:
            serf.x = x
            serf.y = y

    t1 = test1(10, 15)
    t2 = test2(t1, 20)
    t1.x = t2

    serilaised =  ssm.Serialiser(t1).get()
    deserialised = ssm.Constructor(serilaised).get()
    print("local context STATUS:", {True:"Good", False:"Bad"}[t1.x.y == deserialised.x.y])







