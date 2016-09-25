
from pymjin2 import *

TILE_MODEL           = "models/tile.osgt"
TILE_PREFIX_MATERIAL = "tile0"

class TilesImpl(object):
    def __init__(self, c, nodeName):
        self.c = c
        self.nodeParent = nodeName
        self.tiles = { }
        self.c.provide("tile..position", self.setPosition)
    def __del__(self):
        self.c = None
    def createTileOnce(self, tileName):
        if (tileName in self.tiles):
            return
        self.c.set("node.$SCENE.$TILE.parent", self.nodeParent)
        self.c.set("node.$SCENE.$TILE.model",  TILE_MODEL)
        # Default material.
        mat = TILE_PREFIX_MATERIAL + "1"
        self.c.set("node.$SCENE.$TILE.material", mat)
    def deleteTile(self, tileName):
        self.c.setConst("TILE", tileName)
        self.c.set("node.$SCENE.$TILE.parent", "")
    def setPosition(self, key, value):
        tileName = key[1]
        self.c.setConst("TILE", tileName)
        self.createTileOnce(tileName)
        # Convert "depth row column" into "x y z".
        p = value[0].split(" ")
        pos = "{0} {1} {2}".format(p[2], p[1], p[0])
        self.c.set("node.$SCENE.$TILE.position", pos)

class Tiles(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Tiles")
        self.c.setConst("SCENE", sceneName)
        self.c.setConst("NODE",  nodeName)
        self.impl = TilesImpl(self.c, nodeName)
    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Tiles(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

