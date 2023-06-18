from OpenGL.GL import *
import numpy as np
from shape.geometricShape import GeometricShape

class Sphere(GeometricShape):

    def __init__(self, position, eulers):
        super().__init__(position, eulers)
