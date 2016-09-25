
from pymjin2 import *

MAIN_SEQUENCE_START = "sequence.default.start"
# BEGIN FEATURE MAIN_SOUND_START
MAIN_SOUND_START_API = "main.replaySoundStart"
MAIN_SOUND_START     = "soundBuffer.default.start"
# END FEATURE MAIN_SOUND_START
# BEGIN FEATURE MAIN_LAYOUT
#MAIN_LAYOUT     = "X_shaped"
MAIN_LAYOUT     = "test"
MAIN_LAYOUT_API = "main.loadLayout"
MAIN_LAYOUT_DIR = "layouts"
MAIN_LAYOUT_EXT = "layout"
MAIN_RESOLVER   = "pathResolver.MainResolver"
# END FEATURE MAIN_LAYOUT
# BEGIN FEATURE MAIN_LAYOUT_TILES
MAIN_LAYOUT_TILES_API = "main.createTiles"
# END FEATURE MAIN_LAYOUT_TILES
# BEGIN FEATURE CENTER_TILES
MAIN_CENTER_TILES_API = "main.centerTiles"
# END FEATURE CENTER_TILES
# BEGIN FEATURE IDENTIFY_TILES
MAIN_TILE_IDS     = [1, 2, 3, 4, 5, 6, 7, 8, 9]
MAIN_TILE_IDS_API = "main.identifyTiles"
# END FEATURE IDENTIFY_TILES
# BEGIN FEATURE MAIN_SOUND_SELECTION
MAIN_SOUND_SELECTION_API = "main.replaySoundSelection"
MAIN_SOUND_SELECTION     = "soundBuffer.default.selection"
# END FEATURE MAIN_SOUND_SELECTION
# BEGIN FEATURE MAIN_SOUND_MATCH
MAIN_SOUND_MATCH_API = "main.replaySoundMatch"
MAIN_SOUND_MATCH     = "soundBuffer.default.match"
# END FEATURE MAIN_SOUND_MATCH
# BEGIN FEATURE CHECK_RESULT
MAIN_RESULT_API              = "main.checkResult"
MAIN_RESULT_SEQUENCE_LOSS    = "sequence.default.loss"
MAIN_RESULT_SEQUENCE_VICTORY = "sequence.default.victory"
# END FEATURE CHECK_RESULT
# BEGIN FEATURE MAIN_SOUND_LOSS_VICTORY
MAIN_SOUND_LOSS_API    = "main.replaySoundLoss"
MAIN_SOUND_LOSS        = "soundBuffer.default.loss"
MAIN_SOUND_VICTORY_API = "main.replaySoundVictory"
MAIN_SOUND_VICTORY     = "soundBuffer.default.victory"
# END FEATURE MAIN_SOUND_LOSS_VICTORY
# BEGIN FEATURE MAIN_LOSE_WIN
MAIN_LOSE      = "rotate.default.lose"
MAIN_LOSE_API  = "main.lose"
MAIN_LOSE_NODE = "camera"
MAIN_WIN       = "move.default.drop"
MAIN_WIN_API   = "main.dropVictoryTile"
MAIN_WIN_NODE  = "victory"
# END FEATURE MAIN_LOSE_WIN

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
# BEGIN FEATURE CENTER_TILES
        self.c.provide(MAIN_CENTER_TILES_API, self.setCenterTiles)
# END FEATURE CENTER_TILES
# BEGIN FEATURE IDENTIFY_TILES
        self.c.provide(MAIN_TILE_IDS_API, self.setIdentifyTiles)
# END FEATURE IDENTIFY_TILES
# BEGIN FEATURE MAIN_SOUND_SELECTION
        self.c.setConst("SNDSELECTION", MAIN_SOUND_SELECTION)
        self.c.provide(MAIN_SOUND_SELECTION_API, self.setReplaySoundSelection)
# END FEATURE MAIN_SOUND_SELECTION
# BEGIN FEATURE MAIN_SOUND_MATCH
        self.c.setConst("SNDMATCH", MAIN_SOUND_MATCH)
        self.c.provide(MAIN_SOUND_MATCH_API, self.setReplaySoundMatch)
# END FEATURE MAIN_SOUND_MATCH
# BEGIN FEATURE CHECK_RESULT
        self.c.provide(MAIN_RESULT_API, self.setCheckResult)
        self.c.setConst("SEQLOSS",    MAIN_RESULT_SEQUENCE_LOSS)
        self.c.setConst("SEQVICTORY", MAIN_RESULT_SEQUENCE_VICTORY)
# END FEATURE CHECK_RESULT
# BEGIN FEATURE MAIN_SOUND_LOSS_VICTORY
        self.c.provide(MAIN_SOUND_LOSS_API,    self.setReplaySoundLoss)
        self.c.provide(MAIN_SOUND_VICTORY_API, self.setReplaySoundVictory)
        self.c.setConst("SNDLOSS",    MAIN_SOUND_LOSS)
        self.c.setConst("SNDVICTORY", MAIN_SOUND_VICTORY)
# END FEATURE MAIN_SOUND_LOSS_VICTORY
# BEGIN FEATURE MAIN_LOSE_WIN
        self.c.provide(MAIN_LOSE_API, self.setLose)
        self.c.setConst("LOSE",      MAIN_LOSE)
        self.c.setConst("LOSE_NODE", MAIN_LOSE_NODE)
        self.c.provide(MAIN_WIN_API, self.setDropTile)
        self.c.setConst("WIN",      MAIN_WIN)
        self.c.setConst("WIN_NODE", MAIN_WIN_NODE)
        self.c.listen("$WIN.$SCENE..active", "0", self.onDroppedTile)
        self.vchildren = []
# END FEATURE MAIN_LOSE_WIN
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
# BEGIN FEATURE CENTER_TILES
    def setCenterTiles(self, key, value):
        dim = self.c.get("layout.dimensions")
        self.c.set("tiles.center", dim)
        self.c.report(MAIN_CENTER_TILES_API, "0")
# END FEATURE CENTER_TILES
# BEGIN FEATURE IDENTIFY_TILES
    def setIdentifyTiles(self, key, value):
        positions = self.c.get("layout.positions")
        i = 1
        vpos = list(positions)
        # Distribute IDs so that each ID has a pair.
        while (len(vpos)):
            i = i + 1
            positionID = rand() % len(vpos)
            idsID = i / 2 - 1
            # Reset i.
            if (idsID >= len(MAIN_TILE_IDS)):
                i = 2
                idsID = 0
            pos = vpos[positionID]
            id = MAIN_TILE_IDS[idsID]
            # Assign.
            self.c.setConst("TILE", pos)
            self.c.set("tile.$TILE.id", str(id))
            del vpos[positionID]
        self.c.report(MAIN_TILE_IDS_API, "0")
# END FEATURE IDENTIFY_TILES
# BEGIN FEATURE MAIN_SOUND_SELECTION
    def setReplaySoundSelection(self, key, value):
        self.c.set("$SNDSELECTION.state", "play")
        self.c.report(MAIN_SOUND_SELECTION_API, "0")
# END FEATURE MAIN_SOUND_SELECTION
# BEGIN FEATURE MAIN_SOUND_MATCH
    def setReplaySoundMatch(self, key, value):
        self.c.set("$SNDMATCH.state", "play")
        self.c.report(MAIN_SOUND_MATCH_API, "0")
# END FEATURE MAIN_SOUND_MATCH
# BEGIN FEATURE CHECK_RESULT
    def setCheckResult(self, key, value):
        (hasTiles, hasMatches) = self.c.get("tiles.stats")
        if (hasTiles == "0"):
            print "Victory"
            self.c.set("$SEQVICTORY.active", "1")
        elif (hasMatches == "0"):
            print "Loss"
            self.c.set("$SEQLOSS.active", "1")
        self.c.report(MAIN_RESULT_API, "0")
# END FEATURE CHECK_RESULT
# BEGIN FEATURE MAIN_SOUND_LOSS_VICTORY
    def setReplaySoundLoss(self, key, value):
        self.c.set("$SNDLOSS.state", "play")
        self.c.report(MAIN_SOUND_LOSS_API, "0")
    def setReplaySoundVictory(self, key, value):
        self.c.set("$SNDVICTORY.state", "play")
        self.c.report(MAIN_SOUND_VICTORY_API, "0")
# END FEATURE MAIN_SOUND_LOSS_VICTORY
# BEGIN FEATURE MAIN_LOSE_WIN
    def locateChildrenOnce(self):
        if (len(self.vchildren)):
            return
        self.vchildren = list(self.c.get("node.$SCENE.$WIN_NODE.children"))
    def onDroppedTile(self, key, value):
        self.c.report(MAIN_WIN_API, "0")
    def setLose(self, key, value):
        self.c.set("$LOSE.$SCENE.$LOSE_NODE.active", "1")
        self.c.report(MAIN_LOSE_API, "0")
    def setDropTile(self, key, value):
        self.locateChildrenOnce()
        child = self.vchildren.pop(0)
        self.c.setConst("CHILD", child)
        self.c.set("$WIN.$SCENE.$CHILD.active", "1")
# END FEATURE MAIN_LOSE_WIN
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

