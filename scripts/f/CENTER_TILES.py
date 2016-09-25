# Provide "main.centerTiles" and "tiles.center".
CLASS Main
    PART CONST
        MAIN_CENTER_TILES_API = "main.centerTiles"
    PART INIT
        self.c.provide(MAIN_CENTER_TILES_API, self.setCenterTiles)
    PART IMPL
        def setCenterTiles(self, key, value):
            dim = self.c.get("layout.dimensions")
            self.c.set("tiles.center", dim)
            self.c.report(MAIN_CENTER_TILES_API, "0")
CLASS Tiles
    PART INIT
        self.c.provide("tiles.center", self.setCenter)
    PART IMPL
        def setCenter(self, key, value):
            w = int(value[0])
            h = int(value[1])
            offset = (w / 2.0 * self.tileDim[0] / 2.0,
                      h / 2.0 * self.tileDim[1] / 2.0 - self.tileDim[1])
            pos = "{0} {1} 0".format(-offset[0], -offset[1])
            self.c.set("node.$SCENE.$NODE.position", pos)
