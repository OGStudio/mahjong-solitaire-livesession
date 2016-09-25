
from pymjin2 import *

LAYOUT_DEFAULT_WIDTH  = 32
LAYOUT_DEFAULT_HEIGHT = 16
LAYOUT_PREFIX_VERSION = "kmahjongg-layout-v"
# Layout 1.1 related prefixes.
LAYOUT_PREFIX_DEPTH   = "d"
LAYOUT_PREFIX_HEIGHT  = "h"
LAYOUT_PREFIX_WIDTH   = "w"
# MJIN2_FEATURE LAYOUT_ERRORS/CONST

class LayoutImpl(object):
    def __init__(self, c):
        self.c = c
        self.positions = []
        self.c.provide("layout.parseFileName", self.setParseFileName)
        self.c.provide("layout.positions", None, self.pos)
        # MJIN2_FEATURE LAYOUT_DIMENSIONS/INIT
        # MJIN2_FEATURE LAYOUT_ERRORS/INIT
    def __del__(self):
        self.c = None
    # MJIN2_FEATURE LAYOUT_DIMENSIONS/IMPL
    # MJIN2_FEATURE LAYOUT_ERRORS/IMPL
    def parseFields(self, fields, width, height):
        self.positions = []
        for i in xrange(0, len(fields)):
            field = fields[i]
            for row in xrange(0, height - 1):
                for column in xrange(0, width - 1):
                    # Detect tile.
                    if ((field[row][column]         == "1") and
                        (field[row][column + 1]     == "2") and
                        (field[row + 1][column]     == "4") and
                        (field[row + 1][column + 1] == "3")):
                        self.positions.append("{0} {1} {2}".format(i,
                                                                   row,
                                                                   column))
    def parseLines(self, lines):
        # MJIN2_FEATURE LAYOUT_ERRORS/RESET
        # Field dimensions.
        depth  = 0
        height = LAYOUT_DEFAULT_HEIGHT
        width  = LAYOUT_DEFAULT_WIDTH
        # Buffers.
        fieldLines = []
        fieldLineID = 0
        fields = []
        # Parse.
        for ln in lines:
            # Ignore comment.
            if ln.startswith("#"):
                continue
            sln = ln.strip()
            # BEGIN Constants.
            if sln.startswith(LAYOUT_PREFIX_VERSION):
                version = sln.split(LAYOUT_PREFIX_VERSION)[1]
                # MJIN2_FEATURE LAYOUT_ERRORS/VERSION
            elif sln.startswith(LAYOUT_PREFIX_DEPTH):
                depth = int(sln.split(LAYOUT_PREFIX_DEPTH)[1])
            elif sln.startswith(LAYOUT_PREFIX_HEIGHT):
                height = int(sln.split(LAYOUT_PREFIX_HEIGHT)[1])
            elif sln.startswith(LAYOUT_PREFIX_WIDTH):
                width = int(sln.split(LAYOUT_PREFIX_WIDTH)[1])
            # END Constants.
            # BEGIN Field.
            else:
                fieldLines.append(sln)
                fieldLineID = fieldLineID + 1
                if (fieldLineID >= height):
                    # Collect field layers.
                    fields.append(fieldLines)
                    # Reset buffers.
                    fieldLines = []
                    fieldLineID = 0
            # END Field.
        # MJIN2_FEATURE LAYOUT_DIMENSIONS/ASSIGN
        # MJIN2_FEATURE LAYOUT_ERRORS/DEPTH
        self.parseFields(fields, width, height)
        # MJIN2_FEATURE LAYOUT_ERRORS/EVEN
    def pos(self, key):
        return self.positions
    def setParseFileName(self, key, value):
        fileName = value[0]
        with open(fileName, "r") as f:
            lines = f.readlines()
            self.parseLines(lines)

class Layout(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Layout")
        self.c.setConst("SCENE", sceneName)
        self.c.setConst("NODE",  nodeName)
        self.impl = LayoutImpl(self.c)
    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Layout(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

