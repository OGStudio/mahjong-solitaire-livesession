# Provide "layout.dimensions".
CLASS Layout
    PART INIT
        self.c.provide("layout.dimensions", None, self.dimensions)
        self.dim = ["0", "0"]
    PART IMPL
        def dimensions(self, key):
            return self.dim
    PART ASSIGN
        self.dim = [str(width),
                    str(height)]
