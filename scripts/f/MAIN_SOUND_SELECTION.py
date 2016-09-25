# Provide "main.replaySoundSelection".
CLASS Main
    PART CONST
        MAIN_SOUND_SELECTION_API = "main.replaySoundSelection"
        MAIN_SOUND_SELECTION     = "soundBuffer.default.selection"
    PART INIT
        self.c.setConst("SNDSELECTION", MAIN_SOUND_SELECTION)
        self.c.provide(MAIN_SOUND_SELECTION_API, self.setReplaySoundSelection)
    PART IMPL
        def setReplaySoundSelection(self, key, value):
            self.c.set("$SNDSELECTION.state", "play")
            self.c.report(MAIN_SOUND_SELECTION_API, "0")
