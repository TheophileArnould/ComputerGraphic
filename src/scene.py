from player import Player
from shape.cube import Cube
import numpy as np
from textureAndLight.light import Light
from shape.sphere import Sphere
import random as rd


class Scene:

    def __init__(self):

        '''
            TO DO render target
            TO DO render ground
            TO DO render arrows
        
        '''
        
        self.sky = []

        self.targets = []

        self.arrows = []

        self.player = Player(position = [2,4,2])

        self.ground = []

        self.lights = []

        self.sky.append(Cube(
            position = [0,0,0],
            eulers = [1,0,0]
            )
        )

        self.targets.append(Cube(
            position = [0,0,3],
            eulers = [0,0,0]
            )
        )
        
        
        
        self.ground.append(Cube(
            position = [0,0,0],
            eulers = [1,1,1]
            )
        )

        self.lights.append(Light(
            [30,-30,25],
            [1,0.8,0.8],
            1
        )
        )
        self.lights.append(Light(
            [15,-15,8],
            [1,0.6,0],
            100
            )
        )

        self.night_mode = False


        
    def update(self,speed):
        self.moveArrows(speed)

   
    def move_player(self, dPos : list[2]):
        dPos = np.array(dPos, dtype = np.float32) * 0.15
        self.player.position[0] += dPos[0]
        self.player.position[1] += dPos[1]

      
    def spin_player(self, dTheta, dPhi):

        self.player.theta += dTheta * 0.1
        if self.player.theta > 360:
            self.player.theta -= 360
        elif self.player.theta <0:
            self.player.theta += 360
        
        self.player.phi = min(
            89, max(-89, self.player.phi + dPhi * 0.1)
        )

        self.player.update_vectors()

    def addArrow(self):
        arrow = Cube(
            position=self.player.position,
            eulers=self.player.rotate,
            direction=self.player.forwards
        )
        self.arrows.append(arrow)#TODO ajouter la fleche avec la direction

    def moveArrows(self,speed):
        for arrow in self.arrows:
            for target in self.targets :
                if(arrow.position[2]> 0.8 and np.linalg.norm(target.position-arrow.position) > 0.8 ):
                    arrow.position += arrow.direction * speed
                    arrow.direction[2] -= 0.01   #Gravité donc accélération vers le bas

    
    def update(self, speed):
        self.moveArrows(speed)
        if self.night_mode:
            self.turnOnNightMode()
        else:
            self.turnOffNightMode()

    def turnOnNightMode(self):
        # Modifier les paramètres d'éclairage pour le mode nuit
        for light in self.lights:
            light.intensity = 0.1  # Réduire l'intensité lumineuse
            light.color = [0.2, 0.2, 0.4]  # Changer la couleur de la lumière en bleu foncé
        # Modifier la couleur du ciel
        for cube in self.sky:
            cube.color = [0, 0, 0.2]  # Changer la couleur du cube du ciel en bleu foncé

    def turnOffNightMode(self):
        # Restaurer les paramètres d'éclairage par défaut
        for light in self.lights:
            light.intensity = 1.0  # Rétablir l'intensité lumineuse par défaut
            light.color = [1, 1, 1]  # Rétablir la couleur de la lumière par défaut
        # Restaurer la couleur du ciel par défaut
        for cube in self.sky:
            cube.color = [0.5, 0.7, 1]  # Rétablir la couleur du cube du ciel en bleu clair

    def changeNightMode(self, direction):
        if direction == "up":
            self.night_mode = False  # Se rapprocher de jour
        elif direction == "down":
            self.night_mode = True  # Se rapprocher de la nuit



