from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

def CreateShader(vertexFilepath, fragmentFilepath):

    with open(vertexFilepath, 'r') as f:
        vertex_src = f.readlines()

    with open(fragmentFilepath, 'r') as f:
        fragment_src = f.readlines()

    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )

    return shader