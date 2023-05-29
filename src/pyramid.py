import OpenGL.GL as GL
import numpy as np


from shape import Shape


class Pyramid(Shape):
    def __init__(self, shader):
        super().__init__(shader)

        # pyramid vertex positions
        positions = np.array((
            # base
            (-0.5, -0.5, -0.5),
            (0.5, -0.5, -0.5),
            (0.5, -0.5, 0.5),
            (-0.5, -0.5, 0.5),
            # top
            (0, 0.5, 0)
        ), dtype=np.float32)

        # pyramid indices
        indices = np.array((
            # base
            0, 1, 2,
            2, 3, 0,
            # sides
            0, 4, 1,
            1, 4, 2,
            2, 4, 3,
            3, 4, 0
        ), dtype=np.uint32)

        self.glid = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.glid)

        self.buffers = GL.glGenBuffers(2)

        # position attribute
        loc = GL.glGetAttribLocation(shader.glid, 'position')
        GL.glEnableVertexAttribArray(loc)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, positions, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)

        # index buffer
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[1])
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)

    def draw(self, model, view, projection):
        GL.glUseProgram(self.shader.glid)
        GL.glBindVertexArray(self.glid)

        super().draw(model, view, projection)

        GL.glDrawElements(GL.GL_TRIANGLES, 18, GL.GL_UNSIGNED_INT, None)