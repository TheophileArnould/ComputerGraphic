from OpenGL.GL import *
import numpy as np
from shape.geometricShape import GeometricShape

class Cube(GeometricShape):

    def __init__(self, position, eulers=[0, 0, 0], direction=[1, 0, 0]):
        super().__init__(position, eulers)
        self.direction = np.array(direction, dtype=np.float32)

