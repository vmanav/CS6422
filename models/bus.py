# Represents a Bus in the System
class Bus:
    def __init__(self, c, stop=0):
        self.c = c
        self.stop = stop
        self.pssngrs = []
