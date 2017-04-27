import time

class pos:
    def __init__(self, x, y, z):
        self.x = str(x)
        self.y = str(y)
        self.z = str(z)

def movelist(poslist, host):
    for pos in poslist:
        time.sleep(0.05)
        host.sendCommand("tp " + pos.x + " " + pos.y + " " + pos.z)

def testmove(host):
    time.sleep(2)
    poslist = list()
    poslist.append(pos(0, 228, 0))
    poslist.append(pos(0, 229, 0))
    poslist.append(pos(0, 230, 0))
    poslist.append(pos(0, 231, 0))
    poslist.append(pos(0, 232, 0))
    poslist.append(pos(0, 231, 0))
    poslist.append(pos(0, 230, 0))
    poslist.append(pos(0, 229, 0))
    poslist.append(pos(0, 228, 0))
    movelist(poslist, host)
