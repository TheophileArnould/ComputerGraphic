from OpenGL.GL import *
import numpy as np
import math

class SphereMesh():
    def __init__(self, sector_count=36, stack_count=18):

        self.sector_count = sector_count
        self.stack_count = stack_count

        self.vertices = []
        self.normals = []
        self.indices = []

        self.__build_vertices()
        self.vertex_count = len(self.vertices)
        self.__build_indices()

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(3)

        # position attribute
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        # normal attribute
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
        glBufferData(GL_ARRAY_BUFFER, self.normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, False, 0, None)

        # index buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo[2])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)

    def __build_vertices(self):
        # Clear the vertex list
        self.vertices.clear()
        self.normals.clear()

        radius = 0.5
        x, y, z = 0, 0, 0

        sector_step = 2 * math.pi / self.sector_count
        stack_step = math.pi / self.stack_count

        for i in range(self.stack_count + 1):
            stack_angle = math.pi / 2 - i * stack_step
            xy = radius * math.cos(stack_angle)
            z = radius * math.sin(stack_angle)

            for j in range(self.sector_count + 1):
                sector_angle = j * sector_step
                x = xy * math.cos(sector_angle)
                y = xy * math.sin(sector_angle)
                vertex = [x, y, z]
                normal = np.array(vertex, dtype=np.float32)
                normal /= np.linalg.norm(normal)
                self.vertices.append(vertex)
                self.normals.append(normal)
        
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.normals = np.array(self.normals, dtype=np.float32)

    def __build_indices(self):
        # Clear the index list
        self.indices.clear()

        k1, k2 = 0, 0

        for i in range(self.stack_count):
            k1 = i * (self.sector_count + 1)
            k2 = k1 + self.sector_count + 1

            for j in range(self.sector_count):
                if i != 0:
                    self.indices.append(k1)
                    self.indices.append(k2)
                    self.indices.append(k1 + 1)

                if i != (self.stack_count - 1):
                    self.indices.append(k1 + 1)
                    self.indices.append(k2)
                    self.indices.append(k2 + 1)

                k1 += 1
                k2 += 1

        self.indices = np.array(self.indices,dtype=np.float32)

    """
    def draw(self, model, view, projection):
        glUseProgram(self.shader.glid)
        glBindVertexArray(self.glid)

        super().draw(model, view, projection)

        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
    """

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
