import numpy as np
import OpenGL.GL as GL

from cylinder import Cylinder

import glm
from glfw import get_time


class Target(Cylinder):
    def __init__(self, shader, height=1.0, radius=0.5, slices=16):
        super().__init__(shader,height,radius,slices)

        '''self.loc_diffuse_map = GL.glGetUniformLocation(shader.glid, 'diffuse_map')
        # setup texture and upload it to GPU
        self.texture = texture
        '''


    def draw(self, model, view, projection):

        rot_mat = glm.rotate(45+get_time(), glm.vec3(0, 1, 0))
        tra_mat = glm.translate(glm.vec3(0, 0, -3))
        sca_mat = glm.scale(glm.vec3(1, 1, 1))
        
        view = np.array(tra_mat @ rot_mat @ sca_mat)

        super().draw(model, view, projection)

        '''
        # texture access setups
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.glid)
        GL.glUniform1i(self.loc_diffuse_map, 0)
        super().draw(model, view, projection)

        # leave clean state for easier debugging
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glUseProgram(0)
'''


