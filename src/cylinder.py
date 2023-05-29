import numpy as np
import OpenGL.GL as GL

from shape import Shape

class Cylinder(Shape):
    def __init__(self, shader, height=1.0, radius=0.5, slices=16):
        super().__init__(shader)

        # generate vertices
        vertices = []
        for i in range(slices):
            theta = 2.0 * np.pi * float(i) / float(slices)
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            vertices.append([x, y, 0.5 * height])
            vertices.append([x, y, -0.5 * height])

        # add top and bottom vertices
        vertices.append([0.0, 0.0, 0.5 * height])
        vertices.append([0.0, 0.0, -0.5 * height])

        # generate indices
        indices = []
        for i in range(slices):
            indices.append(2 * i)
            indices.append(2 * i + 1)
            indices.append((2 * i + 2) % (2 * slices))
            indices.append(2 * i + 1)
            indices.append((2 * i + 3) % (2 * slices))
            indices.append((2 * i + 2) % (2 * slices))
            indices.append(2 * i)
            indices.append((2 * i + 2) % (2 * slices))
            indices.append(-2)
            indices.append(2 * i + 1)
            indices.append(-1)

        # convert to numpy arrays
        vertices = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)

        # create vertex buffer
        loc = GL.glGetAttribLocation(shader.glid, 'position')
        GL.glEnableVertexAttribArray(loc)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)

        # create index buffer
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[1])
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)

        self.num_indices = len(indices)

    def draw(self, model, view, projection):
        GL.glUseProgram(self.shader.glid)
        GL.glBindVertexArray(self.glid)

        super().draw(model, view, projection)

        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.num_indices, GL.GL_UNSIGNED_INT, None)
