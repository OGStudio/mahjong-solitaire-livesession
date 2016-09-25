
from pymjin2 import *

TILE_MODEL           = "models/tile.osgt"
TILE_PREFIX_MATERIAL = "tile0"
# BEGIN FEATURE TILES_AVAILABILITY
TILES_AVAILABILITY_API    = "tiles.refreshAvailability"
TILE_MATERIAL_UNAVAILABLE = "tile0{0}_unavailable"
# END FEATURE TILES_AVAILABILITY
# BEGIN FEATURE TILES_SELECTION
TILE_SEQUENCE_SELECTION = "sequence.default.tileSelection"
# END FEATURE TILES_SELECTION
# BEGIN FEATURE TILES_SELECTION_MARK
TILE_MARKED_API      = "tiles.markSelectedTile"
TILE_MARKED_MATERIAL = "tile0{0}_selected"
# END FEATURE TILES_SELECTION_MARK
# BEGIN FEATURE TILES_SELECTION_MATCH
TILE_DELETE_API             = "tiles.deleteMatched"
TILE_MATCH_API              = "tiles.match"
TILE_SEQUENCE_MATCH_SUCCESS = "sequence.default.matchSuccess"
# END FEATURE TILES_SELECTION_MATCH
# BEGIN FEATURE CHECK_RESULT
TILES_STATS_API = "tiles.stats"
# END FEATURE CHECK_RESULT

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
# BEGIN FEATURE TILES_SELECTION
        self.c.setConst("SEQSELECT", TILE_SEQUENCE_SELECTION)
        self.c.listen("node.$SCENE..selected", None, self.onTileSelection)
        self.lastSelectedTile = None
# END FEATURE TILES_SELECTION
# BEGIN FEATURE TILES_SELECTION_MARK
        self.c.provide(TILE_MARKED_API, self.setMarkSelectedTile)
        self.lastMarkedTile = None
# END FEATURE TILES_SELECTION_MARK
# BEGIN FEATURE TILES_SELECTION_MATCH
        self.c.provide(TILE_DELETE_API, self.setDelete)
        self.c.provide(TILE_MATCH_API, self.setMatch)
        self.c.setConst("SEQMATCH", TILE_SEQUENCE_MATCH_SUCCESS)
        self.lastMatchedTile = None
        self.matchedTiles = []
# END FEATURE TILES_SELECTION_MATCH
# BEGIN FEATURE CHECK_RESULT
        self.c.provide(TILES_STATS_API, None, self.stats)
# END FEATURE CHECK_RESULT
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
# BEGIN FEATURE TILES_SELECTION
    def onTileSelection(self, key, value):
        self.lastSelectedTile = key[2]
        self.c.set("$SEQSELECT.active", "1")
# END FEATURE TILES_SELECTION
# BEGIN FEATURE TILES_SELECTION_MARK
    def setMarkSelectedTile(self, key, value):
        tileName = self.lastSelectedTile
        if (self.lastMarkedTile):
            # Do nothing.
            if (tileName == self.lastMarkedTile):
                self.c.report(TILE_MARKED_API, "0")
                return
            # Deselect previously selected tile.
            self.setTileMarked(self.lastMarkedTile, False)
        # Select tile.
        self.setTileMarked(tileName, True)
        self.lastMarkedTile = tileName
        self.c.report(TILE_MARKED_API, "0")
    def setTileMarked(self, tileName, state):
        id = self.ids[tileName]
        mat = TILE_PREFIX_MATERIAL + str(id)
        if (state):
            mat = TILE_MARKED_MATERIAL.format(id)
        self.c.setConst("TILE", tileName)
        self.c.set("node.$SCENE.$TILE.material", mat)
# END FEATURE TILES_SELECTION_MARK
# BEGIN FEATURE TILES_SELECTION_MATCH
    def setDelete(self, key, value):
        for tileName in self.matchedTiles:
            self.deleteTile(tileName)
        self.c.report(TILE_DELETE_API, "0")
    def setMatch(self, key, value):
        self.matchedTiles = []
        # Try to match.
        if (self.lastMatchedTile):
            # Do nothing.
            if (self.lastMatchedTile == self.lastSelectedTile):
                self.c.report(TILE_MATCH_API, "0")
                return
            id1 = self.ids[self.lastMatchedTile]
            id2 = self.ids[self.lastSelectedTile]
            # Successful match.
            if (id1 == id2):
                self.matchedTiles = [self.lastMatchedTile,
                                     self.lastSelectedTile]
        self.lastMatchedTile = self.lastSelectedTile
        # Report match.
        if (len(self.matchedTiles)):
            self.c.set("$SEQMATCH.active", "1")
        self.c.report(TILE_MATCH_API, "0")
# END FEATURE TILES_SELECTION_MATCH
# BEGIN FEATURE CHECK_RESULT
    def stats(self, key):
        hasTiles   = len(self.ids) > 0
        hasMatches = False
        # Find out if there is at least one pair
        # of matching tiles available.
        ids = { }
        for tileName in self.available:
            id = self.ids[tileName]
            if (id not in ids):
                ids[id] = 0
            ids[id] = ids[id] + 1
            # A pair has been found.
            if (ids[id] > 1):
                hasMatches = True
                break
        return ["1" if hasTiles else "0",
                "1" if hasMatches else "0"]
# END FEATURE CHECK_RESULT
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
# BEGIN FEATURE TILES_SELECTION_MARK
        if (self.lastMarkedTile and
            (self.lastMarkedTile == tileName)):
            self.lastMarkedTile = None
# END FEATURE TILES_SELECTION_MARK
# BEGIN FEATURE TILES_SELECTION_MATCH
        if (self.lastMatchedTile and
            (self.lastMatchedTile == tileName)):
            self.lastMatchedTile = None
# END FEATURE TILES_SELECTION_MATCH
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

