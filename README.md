
# Computer Graphics Projet : Dart game

Members : 
- Arnould Théophile
- Cyril Clovis
- Amouzou Feley Milton

RUN THE PROJECT : python src\game.py, click esc to exit run

## I - Project presentation: 

During this project wit developped a dart game using : Python with OpenGL and GLFW libraries

<img src="https://github.com/philehteo/ComputerGraphic/assets/128708157/c3df8af5-1255-4f7f-933e-65b6b1a48e32" alt="drawing" width="200" height="200"/>
<img src="https://github.com/philehteo/ComputerGraphic/assets/128708157/5e3791d8-fe9a-4aaa-b81c-641f0559d409" alt="drawing" width="250" height="200"/>
<img src="https://github.com/philehteo/ComputerGraphic/assets/128708157/021ea208-d4fe-4931-8a7c-9c85078cd216" alt="drawing" width="250" height="200"/>

GLFW offers a set of routines for managing OpenGL windows and OpenGL for graphics support.

### 1 - All features

```
This project is a simple dart game. You spaw on a world with a target in the center.
 - You can move arround the scene using (zqsd) and the mouse.
 - You can shoot arrow in the target and in the ground using space bar
 - There is a sunset or night sky with according lighting
 - you can switch from night to day using up and down arrows
 - To close the window click escape key
```

#### First, we can move with the classic keys: q, z, s, d

z to go forward, s to go back, q to go left and d for right. Additionally, the mouse cursor indicates where the character is looking.

#### Shoot arrows (arrows are cubes)

Pressing space will shoot arrows. These arrows stick to the target, if they hit it. They also remain on the ground surface:

![tireSurCibleEtSol](https://github.com/philehteo/ComputerGraphic/assets/126386321/443dfc4e-cd71-43f2-8c15-f012d4fe6d11)


#### Night mode 

You can switch between night and day modes by clicking the up or down arrow. The top one is day mode and the bottom night mode:

Day :
<img width="1440" alt="Capture d’écran 2023-06-18 à 21 31 51" src="https://github.com/philehteo/ComputerGraphic/assets/128708157/1482e7b1-f733-4719-9ee0-e19a96065c52">

Night :
<img width="1440" alt="Capture d’écran 2023-06-18 à 21 31 55" src="https://github.com/philehteo/ComputerGraphic/assets/128708157/145d3aa9-2209-48ee-8c88-cdd2bcef13b2">

### 2 - Possible improvment

For this project there could be a few improvements in the details. First we could have separate more accuratly the different classes. For exemple we could have write the function moveplayer in the player class to have a better separation of classes.

Some other details could be :
- having a round target with a texture on a cylinder shape
- change the direction of the dart during fall
- have better light distribution

### 3 - Code explanation
![import ](https://github.com/philehteo/ComputerGraphic/assets/126386321/5911b9cf-8a0a-4f8e-9236-328c9e00246c)


Here is a short summary of the imports and therefore the way each class uses and/or is used by the others.

#### Scene

We are initially interested in the Cube, Player and Light classes.
Thos three classes are container to propely store information that will later be use.

Let's start with the Cube class. This classes represents shapes. These form is characterized by a position, direction and angles: those of Euler. Those attribut allow us to make moving cube with an orientation.

For the Player class, we find the position as an attribute. There are also theta and phi angles.

The Light class is composed of position, color and strength (intensity) attributes. Thos will be given as uniforme for texture and sheder rendering

Once all of these classes have been written, we can move on to the Scene. As we saw during the graphic on the import, this Scene class includes everything related to the visual. Thus, these attributes are the sky, the target, the arrows, the player and the light. Methods are used to change the visual state of objects, such as move_player which changes the location of the player along the x and y axes. There is also, moveArrows which allows to move the arrows and finally the methods allowing to lower the light intensity.

#### GraphicsEngine

We are here interested in the classes CubeMesh, CubeSkyMesh, Material.


Let's start with the CubeMesh class. As we have seen, the graphic elements are composed of lots of small triangles (vertex -> x,y,z). In addition to that, we can apply a texture (s,t) to them and finally we determine the orientation of the surface of a vertex (nx, ny, nz) essential for better rendering of light reflections. We put all that in the vertices list and store them in VBOs. VBAs are there to determine the characteristics of VBOs and how to access them.

For CubeSkyMesh, we need to do a little more work since we used software to determine the list of vertices. We have therefore written the methods necessary for the correct parsing of the file.

The Material class applies a texture to a material.

With these classes, the GraphicsEngine class can work correctly. These methods are responsible for initializing the graphics engine, rendering the scene, and releasing graphics resources. For example, we find the render method. It renders the scene using meshes, textures, shaders and transformation matrices. It iterates through the scene elements (sky, targets, ground, arrows) and applies the necessary transformations to display them correctly on screen.

#### Game

The Game class at the highest level, and is a kind of supervisor. It is mainly responsible for generating the infinite game loop and responding to player events.
