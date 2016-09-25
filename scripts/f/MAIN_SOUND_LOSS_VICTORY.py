# Provide "main.replaySoundLoss", "main.replaySoundVictory".
CLASS Main
    PART CONST
        MAIN_SOUND_LOSS_API    = "main.replaySoundLoss"
        MAIN_SOUND_LOSS        = "soundBuffer.default.loss"
        MAIN_SOUND_VICTORY_API = "main.replaySoundVictory"
        MAIN_SOUND_VICTORY     = "soundBuffer.default.victory"
    PART INIT
        self.c.provide(MAIN_SOUND_LOSS_API,    self.setReplaySoundLoss)
        self.c.provide(MAIN_SOUND_VICTORY_API, self.setReplaySoundVictory)
        self.c.setConst("SNDLOSS",    MAIN_SOUND_LOSS)
        self.c.setConst("SNDVICTORY", MAIN_SOUND_VICTORY)
    PART IMPL
        def setReplaySoundLoss(self, key, value):
            self.c.set("$SNDLOSS.state", "play")
            self.c.report(MAIN_SOUND_LOSS_API, "0")
        def setReplaySoundVictory(self, key, value):
            self.c.set("$SNDVICTORY.state", "play")
            self.c.report(MAIN_SOUND_VICTORY_API, "0")
