# Provide "tiles.refreshAvailability".
CLASS Tiles
    PART CONST
        TILES_AVAILABILITY_API    = "tiles.refreshAvailability"
        TILE_MATERIAL_UNAVAILABLE = "tile0{0}_unavailable"
    PART INIT
        self.c.provide(TILES_AVAILABILITY_API, self.setRefreshAvailability)
        self.available = {}
    PART IMPL
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
    PART DELETE
        del self.available[tileName]
