from OpenGL.GL import *
import numpy as np

class Cube:

    def __init__(self, position, eulers = [0,0,0], direction = [1,0,0]):

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.direction = np.array(direction, dtype=np.float32)

