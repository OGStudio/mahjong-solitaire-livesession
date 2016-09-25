# Provide "main.replaySoundMatch".
CLASS Main
    PART CONST
        MAIN_SOUND_MATCH_API = "main.replaySoundMatch"
        MAIN_SOUND_MATCH     = "soundBuffer.default.match"
    PART INIT
        self.c.setConst("SNDMATCH", MAIN_SOUND_MATCH)
        self.c.provide(MAIN_SOUND_MATCH_API, self.setReplaySoundMatch)
    PART IMPL
        def setReplaySoundMatch(self, key, value):
            self.c.set("$SNDMATCH.state", "play")
            self.c.report(MAIN_SOUND_MATCH_API, "0")
