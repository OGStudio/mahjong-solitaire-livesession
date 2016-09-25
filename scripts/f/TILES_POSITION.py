# Convert raw layout position to world position.
CLASS Tiles
    PART INIT
        # Tile dimensions.
        self.tileDim = []
    PART IMPL
        def calculateTileDimOnce(self):
            if (len(self.tileDim)):
                return
            bb = self.c.get("node.$SCENE.$TILE.bbox")[0].split(" ")
            self.tileDim = [float(bb[1]) - float(bb[0]),
                            float(bb[3]) - float(bb[2]),
                            float(bb[5]) - float(bb[4])]
    PART TRANSLATE
        self.calculateTileDimOnce()
        k = 0.5
        x = float(p[2]) * self.tileDim[0] * k
        y = float(p[1]) * self.tileDim[1] * k
        z = float(p[0]) * self.tileDim[2]
        pos = "{0} {1} {2}".format(x, y, z)
