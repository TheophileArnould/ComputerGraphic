from OpenGL.GL import *
import numpy as np

class CubeMesh:
    
    def __init__(self):
        
        #x, y, z, s, t, nx, ny, nz
        #triangles
        self.vertices = (
                -0.5, -0.5, -0.5, 0, 0, 0, 0, -1,
                 0.5, -0.5, -0.5, 1, 0, 0, 0, -1,
                 0.5,  0.5, -0.5, 1, 1, 0, 0, -1,

                 0.5,  0.5, -0.5, 1, 1, 0, 0, -1,
                -0.5,  0.5, -0.5, 0, 1, 0, 0, -1,
                -0.5, -0.5, -0.5, 0, 0, 0, 0, -1,

                -0.5, -0.5,  0.5, 0, 0, 0, 0, 1,
                 0.5, -0.5,  0.5, 1, 0, 0, 0, 1,
                 0.5,  0.5,  0.5, 1, 1, 0, 0, 1,

                 0.5,  0.5,  0.5, 1, 1, 0, 0, 1,
                -0.5,  0.5,  0.5, 0, 1, 0, 0, 1,
                -0.5, -0.5,  0.5, 0, 0, 0, 0, 1,

                -0.5,  0.5,  0.5, 1, 0, -1, 0, 0,
                -0.5,  0.5, -0.5, 1, 1, -1, 0, 0,
                -0.5, -0.5, -0.5, 0, 1, -1, 0, 0,

                -0.5, -0.5, -0.5, 0, 1, -1, 0, 0,
                -0.5, -0.5,  0.5, 0, 0, -1, 0, 0,
                -0.5,  0.5,  0.5, 1, 0, -1, 0, 0,

                 0.5,  0.5,  0.5, 1, 0, 1, 0, 0,
                 0.5,  0.5, -0.5, 1, 1, 1, 0, 0,
                 0.5, -0.5, -0.5, 0, 1, 1, 0, 0,

                 0.5, -0.5, -0.5, 0, 1, 1, 0, 0,
                 0.5, -0.5,  0.5, 0, 0, 1, 0, 0,
                 0.5,  0.5,  0.5, 1, 0, 1, 0, 0,

                -0.5, -0.5, -0.5, 0, 1, 0, -1, 0,
                 0.5, -0.5, -0.5, 1, 1, 0, -1, 0,
                 0.5, -0.5,  0.5, 1, 0, 0, -1, 0,

                 0.5, -0.5,  0.5, 1, 0, 0, -1, 0,
                -0.5, -0.5,  0.5, 0, 0, 0, -1, 0,
                -0.5, -0.5, -0.5, 0, 1, 0, -1, 0,

                -0.5,  0.5, -0.5, 0, 1, 0, 1, 0,
                 0.5,  0.5, -0.5, 1, 1, 0, 1, 0,
                 0.5,  0.5,  0.5, 1, 0, 0, 1, 0,

                 0.5,  0.5,  0.5, 1, 0, 0, 1, 0,
                -0.5,  0.5,  0.5, 0, 0, 0, 1, 0,
                -0.5,  0.5, -0.5, 0, 1, 0, 1, 0
            )

        self.vertex_count = len(self.vertices) // 8

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        #position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        #texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        #normal
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
    
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))