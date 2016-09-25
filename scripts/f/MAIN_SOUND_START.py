# Provide "main.replaySoundStart".
CLASS Main
    PART CONST
        MAIN_SOUND_START_API = "main.replaySoundStart"
        MAIN_SOUND_START     = "soundBuffer.default.start"
    PART INIT
        self.c.setConst("SNDSTART", MAIN_SOUND_START)
        self.c.provide(MAIN_SOUND_START_API, self.setReplaySoundStart)
    PART IMPL
        def setReplaySoundStart(self, key, value):
            self.c.set("$SNDSTART.state", "play")
            self.c.report(MAIN_SOUND_START_API, "0")
