import OpenGL.GL as GL

class Shape():
    def __init__(self, shader):
        # Initializes a Shape object with a shader program.
        # A vertex array object (VAO) is created and bound to self.glid.
        # Two buffer objects are created to hold data for vertex attributes
        # and element indices, and their ids are stored in self.buffers.
        self.shader = shader
        self.glid = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.glid)
        self.buffers = GL.glGenBuffers(2)

    def draw(self, model, view, projection):
        # This method is meant to be extended by subclasses.
        # It should contain OpenGL calls to draw the shape.

        loc = GL.glGetUniformLocation(self.shader.glid, 'model')
        GL.glUniformMatrix4fv(loc, 1, True, model)

        loc = GL.glGetUniformLocation(self.shader.glid, 'view')
        GL.glUniformMatrix4fv(loc, 1, True, view)

        loc = GL.glGetUniformLocation(self.shader.glid, 'projection')
        GL.glUniformMatrix4fv(loc, 1, True, projection)

    def __del__(self):
        # Deletes the VAO and buffer objects associated with the shape
        # when the object is destroyed.
        GL.glDeleteVertexArrays(1, [self.glid])
        GL.glDeleteBuffers(2, self.buffers)
