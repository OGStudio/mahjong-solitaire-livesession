
from pymjin2 import *

TILE_MODEL           = "models/tile.osgt"
TILE_PREFIX_MATERIAL = "tile0"
# BEGIN FEATURE TILES_AVAILABILITY
TILES_AVAILABILITY_API    = "tiles.refreshAvailability"
TILE_MATERIAL_UNAVAILABLE = "tile0{0}_unavailable"
# END FEATURE TILES_AVAILABILITY

class TilesImpl(object):
    def __init__(self, c, nodeName):
        self.c = c
        self.nodeParent = nodeName
        self.tiles = { }
        self.c.provide("tile..position", self.setPosition)
# BEGIN FEATURE TILES_POSITION
        # Tile dimensions.
        self.tileDim = []
# END FEATURE TILES_POSITION
# BEGIN FEATURE CENTER_TILES
        self.c.provide("tiles.center", self.setCenter)
# END FEATURE CENTER_TILES
# BEGIN FEATURE IDENTIFY_TILES
        self.c.provide("tile..id", self.setTileID, self.tileID)
        self.ids = {}
# END FEATURE IDENTIFY_TILES
# BEGIN FEATURE TILES_AVAILABILITY
        self.c.provide(TILES_AVAILABILITY_API, self.setRefreshAvailability)
        self.available = {}
# END FEATURE TILES_AVAILABILITY
    def __del__(self):
        self.c = None
# BEGIN FEATURE TILES_POSITION
    def calculateTileDimOnce(self):
        if (len(self.tileDim)):
            return
        bb = self.c.get("node.$SCENE.$TILE.bbox")[0].split(" ")
        self.tileDim = [float(bb[1]) - float(bb[0]),
                        float(bb[3]) - float(bb[2]),
                        float(bb[5]) - float(bb[4])]
# END FEATURE TILES_POSITION
# BEGIN FEATURE CENTER_TILES
    def setCenter(self, key, value):
        w = int(value[0])
        h = int(value[1])
        offset = (w / 2.0 * self.tileDim[0] / 2.0,
                  h / 2.0 * self.tileDim[1] / 2.0 - self.tileDim[1])
        pos = "{0} {1} 0".format(-offset[0], -offset[1])
        self.c.set("node.$SCENE.$NODE.position", pos)
# END FEATURE CENTER_TILES
# BEGIN FEATURE IDENTIFY_TILES
    def tileID(self, key):
        tileName = key[1]
        if (tileName in self.ids):
            id = self.ids[tileName]
            return [str(id)]
        # Invalid ID for invalid tile name.
        return ["0"]
    def setTileID(self, key, value):
        tileName = key[1]
        sid = value[0]
        mat = TILE_PREFIX_MATERIAL + sid
        self.c.setConst("TILE", tileName)
        self.c.set("node.$SCENE.$TILE.material", mat)
        # Store.
        self.ids[tileName] = int(sid)
# END FEATURE IDENTIFY_TILES
# BEGIN FEATURE TILES_AVAILABILITY
    def setRefreshAvailability(self, key, value):
        for tileName in self.ids:
            state = self.tileIsAvailable(tileName)
            self.setTileAvailable(tileName, state)
        self.c.report(TILES_AVAILABILITY_API, "0")
    def setTileAvailable(self, tileName, state):
        id = self.ids[tileName]
        mat = TILE_PREFIX_MATERIAL + str(id)
        if (not state):
            mat = TILE_MATERIAL_UNAVAILABLE.format(id)
        self.c.setConst("TILE", tileName)
        # Set corresponding material.
        self.c.set("node.$SCENE.$TILE.material", mat)
        # Make available tile selectable.
        val = ("1" if state else "0")
        self.c.set("node.$SCENE.$TILE.selectable", val)
        # Cache.
        if (state):
            self.available[tileName] = True
        elif (tileName in self.available):
            del self.available[tileName]
    def tileHasNeighbours(self, tileName, offsetDepth, offsetRow):
        p = tileName.split(" ")
        pos = (int(p[0]), int(p[1]), int(p[2]))
        for offsetColumn in xrange(-1, 2):
            neighbourName = "{0} {1} {2}".format(pos[0] + offsetDepth,
                                                 pos[1] + offsetColumn,
                                                 pos[2] + offsetRow)
            if (neighbourName in self.ids):
                return True
        return False
    def tileIsAvailable(self, tileName):
        # Tile is blocked at both sides.
        left  = self.tileHasNeighbours(tileName, 0, -2)
        right = self.tileHasNeighbours(tileName, 0, 2)
        if (left and right):
            return False
        # Tile is blocked at the top.
        for column in xrange(-1, 2):
            if (self.tileHasNeighbours(tileName, 1, column)):
                return False
        # Tile is free.
        return True
# END FEATURE TILES_AVAILABILITY
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
# BEGIN FEATURE IDENTIFY_TILES
        del self.ids[tileName]
# END FEATURE IDENTIFY_TILES
# BEGIN FEATURE TILES_AVAILABILITY
        del self.available[tileName]
# END FEATURE TILES_AVAILABILITY
    def setPosition(self, key, value):
        tileName = key[1]
        self.c.setConst("TILE", tileName)
        self.createTileOnce(tileName)
        # Convert "depth row column" into "x y z".
        p = value[0].split(" ")
        pos = "{0} {1} {2}".format(p[2], p[1], p[0])
# BEGIN FEATURE TILES_POSITION
        self.calculateTileDimOnce()
        k = 0.5
        x = float(p[2]) * self.tileDim[0] * k
        y = float(p[1]) * self.tileDim[1] * k
        z = float(p[0]) * self.tileDim[2]
        pos = "{0} {1} {2}".format(x, y, z)
# END FEATURE TILES_POSITION
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

