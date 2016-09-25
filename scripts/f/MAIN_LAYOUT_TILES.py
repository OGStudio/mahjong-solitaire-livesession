# Provide "main.createTiles".
CLASS Main
    PART CONST
        MAIN_LAYOUT_TILES_API = "main.createTiles"
    PART INIT
        self.c.provide(MAIN_LAYOUT_TILES_API, self.setCreateTiles)
    PART IMPL
        def setCreateTiles(self, key, value):
            positions = self.c.get("layout.positions")
            # Create tiles.
            for p in positions:
                self.c.setConst("TILE", p)
                self.c.set("tile.$TILE.position", p)
            self.c.report(MAIN_LAYOUT_TILES_API, "0")
