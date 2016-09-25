# Provide "main.lose", "main.dropVictoryTile".
CLASS Main
    PART CONST
        MAIN_LOSE      = "rotate.default.lose"
        MAIN_LOSE_API  = "main.lose"
        MAIN_LOSE_NODE = "camera"
        MAIN_WIN       = "move.default.drop"
        MAIN_WIN_API   = "main.dropVictoryTile"
        MAIN_WIN_NODE  = "victory"
    PART INIT
        self.c.provide(MAIN_LOSE_API, self.setLose)
        self.c.setConst("LOSE",      MAIN_LOSE)
        self.c.setConst("LOSE_NODE", MAIN_LOSE_NODE)
        self.c.provide(MAIN_WIN_API, self.setDropTile)
        self.c.setConst("WIN",      MAIN_WIN)
        self.c.setConst("WIN_NODE", MAIN_WIN_NODE)
        self.c.listen("$WIN.$SCENE..active", "0", self.onDroppedTile)
        self.vchildren = []
    PART IMPL
        def locateChildrenOnce(self):
            if (len(self.vchildren)):
                return
            self.vchildren = list(self.c.get("node.$SCENE.$WIN_NODE.children"))
        def onDroppedTile(self, key, value):
            self.c.report(MAIN_WIN_API, "0")
        def setLose(self, key, value):
            self.c.set("$LOSE.$SCENE.$LOSE_NODE.active", "1")
            self.c.report(MAIN_LOSE_API, "0")
        def setDropTile(self, key, value):
            self.locateChildrenOnce()
            child = self.vchildren.pop(0)
            self.c.setConst("CHILD", child)
            self.c.set("$WIN.$SCENE.$CHILD.active", "1")
