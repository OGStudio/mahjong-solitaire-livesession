# Provide "main.loadLayout.
CLASS Main
    PART CONST
        MAIN_LAYOUT     = "X_shaped"
        MAIN_LAYOUT_API = "main.loadLayout"
        MAIN_LAYOUT_DIR = "layouts"
        MAIN_LAYOUT_EXT = "layout"
        MAIN_RESOLVER   = "pathResolver.MainResolver"
    PART INIT
        self.c.setConst("RESOLVER", MAIN_RESOLVER)
        self.c.provide(MAIN_LAYOUT_API, self.setLoadLayout)
    PART IMPL
        def setLoadLayout(self, key, value):
            fileName = "{0}/{1}.{2}".format(MAIN_LAYOUT_DIR,
                                            MAIN_LAYOUT,
                                            MAIN_LAYOUT_EXT)
            self.c.set("$RESOLVER.resolveFileNameAbs", fileName)
            fileNameAbs = self.c.get("$RESOLVER.fileNameAbs")
            self.c.set("layout.parseFileName", fileNameAbs)
            self.c.report(MAIN_LAYOUT_API, "0")
