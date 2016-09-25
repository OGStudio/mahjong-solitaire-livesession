# Provide "tileSelection" sequence.
CLASS Tiles
    PART CONST
        TILE_SEQUENCE_SELECTION = "sequence.default.tileSelection"
    PART INIT
        self.c.setConst("SEQSELECT", TILE_SEQUENCE_SELECTION)
        self.c.listen("node.$SCENE..selected", None, self.onTileSelection)
        self.lastSelectedTile = None
    PART IMPL
        def onTileSelection(self, key, value):
            self.lastSelectedTile = key[2]
            self.c.set("$SEQSELECT.active", "1")
