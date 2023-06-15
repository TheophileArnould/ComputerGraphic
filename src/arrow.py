import pathlib
from shader import Shader
from cylinder import Cylinder

class Arrow(Cylinder):
    #Variable statique
    shaders_dir = str(pathlib.Path().parent.absolute()) + "/shaders/"
    color_shader = Shader(shaders_dir + "color.vert", shaders_dir + "color.frag")
    
    def __init__(self, shader, height, radius, slices):
        super().__init__(shader, height, radius, slices)

    def draw(self, model, view, projection):
        super().draw(model, view, projection)

    @staticmethod
    def generate_cylinder(height=0.8, radius=0.05, slices=16):
        return Arrow(height, radius, slices)