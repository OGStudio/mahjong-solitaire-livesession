# Provide "tiles.markSelectedTile".
CLASS Tiles
    PART CONST
        TILE_MARKED_API      = "tiles.markSelectedTile"
        TILE_MARKED_MATERIAL = "tile0{0}_selected"
    PART INIT
        self.c.provide(TILE_MARKED_API, self.setMarkSelectedTile)
        self.lastMarkedTile = None
    PART IMPL
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
    PART DELETE
        if (self.lastMarkedTile and
            (self.lastMarkedTile == tileName)):
            self.lastMarkedTile = None
