from mesh.cubeMesh import CubeMesh
from mesh.cubeSkyMesh import CubeSkyMesh
from mesh.sphereMesh import SphereMesh
from textureAndLight.material import Material

import pathlib
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import numpy as np

from glfw import get_time

class GraphicsEngine:

    def __init__(self):

        self.perdu = False #True si un des méchants atteint la caméra
        self.renderDistance = 60


        self.cube_mesh = CubeMesh()
        self.cube_sky_mesh = CubeSkyMesh()

        self.textureRock = Material("Images/rock.png")
        self.textureSky = Material("Images/sky.jpg")
        self.textureTarget = Material("Images/target.png")
        self.textureCubeSkyDay = Material("Images/CubeMapRotateRevers.png")
        self.textureCubeSkyNight = Material("Images/nightSky.jpg")

        glClearColor(0.1,0.1,0.1,1)
        glEnable(GL_DEPTH_TEST)
        self.shader = self.CreateShader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 1280/960,
            near = 0.1, far = self.renderDistance, dtype=np.float32
        )

        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )

        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")
        self.viewMatrixLocation = glGetUniformLocation(self.shader, "view")
        self.lightLocation = {
            "position": [
                glGetUniformLocation(self.shader, f"Lights[{i}].position")
                for i in range(8)
            ],
            "color": [
                glGetUniformLocation(self.shader, f"Lights[{i}].color")
                for i in range(8)
            ],
            "strength": [
                glGetUniformLocation(self.shader, f"Lights[{i}].strength")
                for i in range(8)
            ]
        }
        self.cameraPosLoc = glGetUniformLocation(self.shader, "cameraPostion")

    def CreateShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader
    
    
    def render(self, scene):
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader)
            
        view_transform = pyrr.matrix44.create_look_at(
            eye = scene.player.position,
            target = scene.player.position + scene.player.forwards,
            up = scene.player.up, dtype = np.float32
        )

        glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, view_transform)

        dedans = False
        
        for sky in scene.sky:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_scale(
                    scale=np.array([20,20,20], dtype=np.float32),
                    dtype=np.float32
                )
            )
            
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_x_rotation(
                    theta=np.deg2rad(90),
                    dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=sky.position,
                    dtype=np.float32
                )
            )
            CubeSkyMesh()
            if(scene.night_mode):
                self.textureCubeSkyDay.use()
                glUniform1f(glGetUniformLocation(self.shader, "ambientStrenght"), 0.9)
            else:
                self.textureCubeSkyNight.use()
                glUniform1f(glGetUniformLocation(self.shader, "ambientStrenght"), 0.4)
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_sky_mesh.vertex_count)

        for target in scene.targets:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_scale(
                    scale=np.array([1,1,1], dtype=np.float32),
                    dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=target.position,
                    dtype=np.float32
                )
            )

            CubeMesh()
            self.textureTarget.use()
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)
        

        for ground in scene.ground:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_scale(
                    scale=np.array([40,40,1], dtype=np.float32),
                    dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=ground.position,
                    dtype=np.float32
                )
            )
            self.textureRock.use()
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

        if(scene.night_mode):
            for i,light in enumerate(scene.dayLights):
                glUniform3fv(self.lightLocation["position"][i], 1, light.position)
                glUniform3fv(self.lightLocation["color"][i], 1, light.color)
                glUniform1f(self.lightLocation["strength"][i], light.strength)
        else:
            for i,light in enumerate(scene.nightLights):
                glUniform3fv(self.lightLocation["position"][i], 1, light.position)
                glUniform3fv(self.lightLocation["color"][i], 1, light.color)
                glUniform1f(self.lightLocation["strength"][i], light.strength)

        for arrow in scene.arrows:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_scale(
                    scale=np.array([.2,.02,.02], dtype=np.float32),
                    dtype=np.float32
                )
            )
            
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_y_rotation(#TODO depends on phi coordinates (find the calculus)
                    theta=np.deg2rad(arrow.eulers[1]),
                    dtype=np.float32
                )
            )

            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_z_rotation(
                    theta=np.deg2rad(-arrow.eulers[2]),
                    dtype=np.float32
                )
            )            
            
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=arrow.position,
                    dtype=np.float32
                )
            )
            

            self.textureRock.use()
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

        glUniform3fv(self.cameraPosLoc, 1, scene.player.position)


        glFlush()

    def destroy(self):

        self.cube_mesh.destroy()
        self.cube_sky_mesh.destroy()
        self.textureRock.destroy()
        self.textureSky.destroy()
        self.textureTarget.destroy()
        self.textureCubeSkyNight.destroy()
        self.textureCubeSkyDay.destroy()

        glDeleteProgram(self.shader)