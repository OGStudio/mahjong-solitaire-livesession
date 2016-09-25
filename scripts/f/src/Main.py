
from pymjin2 import *

MAIN_SEQUENCE_START = "sequence.default.start"
# MJIN2_FEATURE MAIN_SOUND_START/CONST
# MJIN2_FEATURE MAIN_LAYOUT/CONST
# MJIN2_FEATURE MAIN_LAYOUT_TILES/CONST
# MJIN2_FEATURE CENTER_TILES/CONST
# MJIN2_FEATURE IDENTIFY_TILES/CONST
# MJIN2_FEATURE MAIN_SOUND_SELECTION/CONST
# MJIN2_FEATURE MAIN_SOUND_MATCH/CONST
# MJIN2_FEATURE CHECK_RESULT/CONST
# MJIN2_FEATURE MAIN_SOUND_LOSS_VICTORY/CONST
# MJIN2_FEATURE MAIN_LOSE_WIN/CONST

class MainImpl(object):
    def __init__(self, c):
        self.c = c
        self.isOn = False
        self.c.listen("input.SPACE.key", "1", self.onSpace)
        # MJIN2_FEATURE MAIN_SOUND_START/INIT
        # MJIN2_FEATURE MAIN_LAYOUT/INIT
        # MJIN2_FEATURE MAIN_LAYOUT_TILES/INIT
        # MJIN2_FEATURE CENTER_TILES/INIT
        # MJIN2_FEATURE IDENTIFY_TILES/INIT
        # MJIN2_FEATURE MAIN_SOUND_SELECTION/INIT
        # MJIN2_FEATURE MAIN_SOUND_MATCH/INIT
        # MJIN2_FEATURE CHECK_RESULT/INIT
        # MJIN2_FEATURE MAIN_SOUND_LOSS_VICTORY/INIT
        # MJIN2_FEATURE MAIN_LOSE_WIN/INIT
    def __del__(self):
        self.c = None
    # MJIN2_FEATURE MAIN_SOUND_START/IMPL
    # MJIN2_FEATURE MAIN_LAYOUT/IMPL
    # MJIN2_FEATURE MAIN_LAYOUT_TILES/IMPL
    # MJIN2_FEATURE CENTER_TILES/IMPL
    # MJIN2_FEATURE IDENTIFY_TILES/IMPL
    # MJIN2_FEATURE MAIN_SOUND_SELECTION/IMPL
    # MJIN2_FEATURE MAIN_SOUND_MATCH/IMPL
    # MJIN2_FEATURE CHECK_RESULT/IMPL
    # MJIN2_FEATURE MAIN_SOUND_LOSS_VICTORY/IMPL
    # MJIN2_FEATURE MAIN_LOSE_WIN/IMPL
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

