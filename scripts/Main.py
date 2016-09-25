
from pymjin2 import *

MAIN_SEQUENCE_START = "sequence.default.start"
# BEGIN FEATURE MAIN_SOUND_START
MAIN_SOUND_START_API = "main.replaySoundStart"
MAIN_SOUND_START     = "soundBuffer.default.start"
# END FEATURE MAIN_SOUND_START
# BEGIN FEATURE MAIN_LAYOUT
MAIN_LAYOUT     = "X_shaped"
MAIN_LAYOUT_API = "main.loadLayout"
MAIN_LAYOUT_DIR = "layouts"
MAIN_LAYOUT_EXT = "layout"
MAIN_RESOLVER   = "pathResolver.MainResolver"
# END FEATURE MAIN_LAYOUT
# BEGIN FEATURE MAIN_LAYOUT_TILES
MAIN_LAYOUT_TILES_API = "main.createTiles"
# END FEATURE MAIN_LAYOUT_TILES

class MainImpl(object):
    def __init__(self, c):
        self.c = c
        self.isOn = False
        self.c.listen("input.SPACE.key", "1", self.onSpace)
# BEGIN FEATURE MAIN_SOUND_START
        self.c.setConst("SNDSTART", MAIN_SOUND_START)
        self.c.provide(MAIN_SOUND_START_API, self.setReplaySoundStart)
# END FEATURE MAIN_SOUND_START
# BEGIN FEATURE MAIN_LAYOUT
        self.c.setConst("RESOLVER", MAIN_RESOLVER)
        self.c.provide(MAIN_LAYOUT_API, self.setLoadLayout)
# END FEATURE MAIN_LAYOUT
# BEGIN FEATURE MAIN_LAYOUT_TILES
        self.c.provide(MAIN_LAYOUT_TILES_API, self.setCreateTiles)
# END FEATURE MAIN_LAYOUT_TILES
    def __del__(self):
        self.c = None
# BEGIN FEATURE MAIN_SOUND_START
    def setReplaySoundStart(self, key, value):
        self.c.set("$SNDSTART.state", "play")
        self.c.report(MAIN_SOUND_START_API, "0")
# END FEATURE MAIN_SOUND_START
# BEGIN FEATURE MAIN_LAYOUT
    def setLoadLayout(self, key, value):
        fileName = "{0}/{1}.{2}".format(MAIN_LAYOUT_DIR,
                                        MAIN_LAYOUT,
                                        MAIN_LAYOUT_EXT)
        self.c.set("$RESOLVER.resolveFileNameAbs", fileName)
        fileNameAbs = self.c.get("$RESOLVER.fileNameAbs")
        self.c.set("layout.parseFileName", fileNameAbs)
        self.c.report(MAIN_LAYOUT_API, "0")
# END FEATURE MAIN_LAYOUT
# BEGIN FEATURE MAIN_LAYOUT_TILES
    def setCreateTiles(self, key, value):
        positions = self.c.get("layout.positions")
        # Create tiles.
        for p in positions:
            self.c.setConst("TILE", p)
            self.c.set("tile.$TILE.position", p)
        self.c.report(MAIN_LAYOUT_TILES_API, "0")
# END FEATURE MAIN_LAYOUT_TILES
    def onSpace(self, key, value):
        if self.isOn:
            return
        self.isOn = True
        print "Space pressed. Start the game"
        self.c.setConst("SEQSTART", MAIN_SEQUENCE_START)
        self.c.set("$SEQSTART.active", "1")

class Main(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Main")
        self.c.setConst("SCENE", sceneName)
        self.c.setConst("NODE",  nodeName)
        self.impl = MainImpl(self.c)
    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Main(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

