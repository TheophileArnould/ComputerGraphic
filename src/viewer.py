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
from target import Target
#from arrow import Arrow


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
        #TEST POUR PLUS TARD
        self.view = None
        self.projection = None

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)
        glfw.set_mouse_button_callback(self.win, self.mouse_button_callback)

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
            self.view = view

            projection = array(perspective(45, 1, 0, 10))
            self.projection = projection

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
    
    def mouse_button_callback(self, window, button, action, mods):
        # Vérifiez si le bouton de la souris est le bouton gauche et s'il a été pressé
        if ((action == glfw.PRESS) and (button == glfw.MOUSE_BUTTON_LEFT)):
            # Obtenez les coordonnées de la souris
            x, y = glfw.get_cursor_pos(window)
            self.generate_cylinder(x, y)

    def generate_cylinder(self, x, y):
        shaders_dir = str(pathlib.Path().parent.absolute()) + "/shaders/"
        # Créez une instance de Cylinder avec le shader approprié et les paramètres souhaités
        color_shader = Shader(shaders_dir + "color.vert", shaders_dir + "color.frag")
        cylinder = Cylinder(color_shader, height=1.0, radius=0.5, slices=16)
        # Appliquez une transformation de translation pour positionner le cylindre aux coordonnées (x, y)
        translation_matrix = translate(vec3(x, y, 0.0))
        translation_array = translation_matrix.to_list()  # Convert the matrix to a list
        # Appelez la méthode draw de l'instance de Cylinder en passant les matrices de transformation appropriées
        cylinder.draw(array(translation_array), self.view, self.projection)
        print("(x, y) = ",x, y)


# -------------- main program and scene setup --------------------------------
def main():
    """ create window, add shaders & scene objects, then run rendering loop """
    viewer = Viewer()
    shaders_dir = str(pathlib.Path().parent.absolute()) + "/shaders/"
    color_shader = Shader(shaders_dir + "color.vert", shaders_dir + "color.frag")

    target = Target(color_shader)
    target_transform = scale((1, 1, 0.05))
    target_node = Node(transform=target_transform)
    target_node.add(target)

    #cylindre = Cylinder(color_shader, height=0.8, radius=0.05)
    #cylindre_transform = translate((0, 0.5, 0))
    #cylindre_node = Node(transform=cylindre_transform)
    #cylindre_node.add(cylindre)
    # Add the root node to the scene
    viewer.scene_root.add(target_node)
    #viewer.scene_root.add(cylindre)

    # start the rendering loop
    viewer.run()


# code execution begins here
if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
