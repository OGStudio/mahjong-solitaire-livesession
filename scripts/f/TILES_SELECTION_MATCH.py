# Provide "tiles.deleteMatched", "tiles.match" and "matchSuccess" sequence.
CLASS Tiles
    PART CONST
        TILE_DELETE_API             = "tiles.deleteMatched"
        TILE_MATCH_API              = "tiles.match"
        TILE_SEQUENCE_MATCH_SUCCESS = "sequence.default.matchSuccess"
    PART INIT
        self.c.provide(TILE_DELETE_API, self.setDelete)
        self.c.provide(TILE_MATCH_API, self.setMatch)
        self.c.setConst("SEQMATCH", TILE_SEQUENCE_MATCH_SUCCESS)
        self.lastMatchedTile = None
        self.matchedTiles = []
    PART IMPL
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
    PART DELETE
        if (self.lastMatchedTile and
            (self.lastMatchedTile == tileName)):
            self.lastMatchedTile = None
