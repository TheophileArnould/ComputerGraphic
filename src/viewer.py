#!/usr/bin/env python3

# Python built-in modules
import pathlib

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL

from glm import rotate, translate, scale, perspective, identity, mat4, vec3, radians
from numpy import array

from shader import Shader
from node import Node
from cylinder import Cylinder
from pyramid import Pyramid
from triangle import Triangle


class Viewer:
    """ GLFW viewer window, with classic initialization & graphics loop """

    def __init__(self, width=640, height=480):

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)

        self.scene_root = Node()

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            # clear draw buffer
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)

            model = array(identity(mat4))

            rot_mat = identity(mat4)
            tra_mat = translate(vec3(0, 0, -4))
            sca_mat = identity(mat4)
            view =  array(tra_mat @ rot_mat @ sca_mat)

            projection = array(perspective(45, 1, 0, 10))

            self.scene_root.draw(model, view, projection)

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)


# -------------- main program and scene setup --------------------------------
def main():
    """ create window, add shaders & scene objects, then run rendering loop """
    viewer = Viewer()
    shaders_dir = str(pathlib.Path().parent.absolute()) + "/shaders/"
    color_shader = Shader(shaders_dir + "color.vert", shaders_dir + "color.frag")

    target = Cylinder(color_shader)
    target_transform = translate((0, 1.3, 0)) @ scale((1, 1, 1)) @ rotate(radians(90.0), (0, 1, 1))
    target_node = Node(transform=target_transform)
    target_node.add(target)

    # Add the root node to the scene
    viewer.scene_root.add(target_node)

    # start the rendering loop
    viewer.run()


# code execution begins here
if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
