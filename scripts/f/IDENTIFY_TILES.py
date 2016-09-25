# Provide "main.identifyTiles" and "tile..id".
CLASS Main
    PART CONST
        MAIN_TILE_IDS     = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        MAIN_TILE_IDS_API = "main.identifyTiles"
    PART INIT
        self.c.provide(MAIN_TILE_IDS_API, self.setIdentifyTiles)
    PART IMPL
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
CLASS Tiles
    PART INIT
        self.c.provide("tile..id", self.setTileID, self.tileID)
        self.ids = {}
    PART IMPL
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
    PART DELETE
        del self.ids[tileName]
