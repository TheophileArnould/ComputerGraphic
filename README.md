
# Project Title

This project is a simple dart game. You spaw on a world with a target in the center.
 - You can move arround using (zqsd) and the mouse.
 - You can shoot arrow in the target and in the ground using space bar
 - There is a sunset sky with according lighting
 - To close the window click escape key

Computer Graphics Projet
         Projet Topic : Dart game
Members : 
Arnould Théophile
Cyril Clovis
Amouzou Feley Milton

RUN THE PROJECT : python src\game.py, click esc to exit run

I - Project presentation: 
Through this project we have developed a dart board. To do this we used the Python language.



We used the GLFW library which offers a set of routines for managing OpenGL windows and OpenGL for graphics support.






1 - All features

In this part we will detail an exhaustive list of the functionalities developed

Move around and choose the viewing angle

First, we can move with the classic keys: q, z, s, d
z to go forward, s to go back, q to go left and d for right. Additionally, the mouse cursor indicates where the character is looking.

Shoot arrows (arrows are cubes)

Pressing space will shoot arrows. These arrows stick to the target, if they hit it. They also remain on the ground surface:




decrease/increase brightness

You can toggle between two brightness modes by clicking the up or down arrow. The top one increases the brightness, the bottom one decreases it:



low and high brightness


2 - Code explanation


Here is a short summary of the imports and therefore the way each class uses and/or is used by the others.

 Scene

We are initially interested in the Cube, Sphere, Player and Light classes.

Let's start with the Cube and Sphere class. These two classes represent shapes. These forms are characterized by a position and angles: those of Euler. Thanks to them, we can represent the orientation of the solid through 3 angles (because we can turn on each of the 3 dimensions).

Cube has an additional property, it is the direction. The Sphere class does not need this because it is symmetrical in all directions.

For the Player class, we find the position as an attribute. There are also theta and phi angles. Indeed, the player moves in a 2D plane composed of the horizontal axis x (and its angle theta) and the vertical axis y (and its angle phi). Thanks to the angles, we determine the directional vectors that we use to determine the orientation and the movements of the player.

The Light class is composed of position, color and strength (intensity) attributes.

Once all of these classes have been written, we can move on to the Scene. As we saw during the graphic on the import, this Scene class includes everything related to the visual. Thus, these attributes are the sky, the target, the arrows, the player and the light. Methods are used to change the visual state of objects, such as move_player which changes the location of the player along the x and y axes. There is also, moveArrows which allows to move the arrows and finally the methods allowing to lower the light intensity.

GraphicsEngine

We are initially interested in the classes CubeMesh, CubeSkyMesh, SphereMesh and Material.

Let's start with the CubeMesh class. As we have seen, the graphic elements are composed of lots of small triangles (vertex -> x,y,z). In addition to that, we can apply a texture (s,t) to them and finally we determine the orientation of the surface of a vertex (nx, ny, nz) essential for better rendering of light reflections. We put all that in the vertices list and store them in VBOs. VBAs are there to determine the characteristics of VBOs and how to access them.

For CubeSkyMesh, we need to do a little more work since we used software to determine the list of vertices. We have therefore written the methods necessary for the correct parsing of the file.

The Material class applies a texture to a material.

With these classes, the GraphicsEngine class can work correctly. These methods are responsible for initializing the graphics engine, rendering the scene, and releasing graphics resources. For example, we find the render method. It renders the scene using meshes, textures, shaders and transformation matrices. It iterates through the scene elements (sky, targets, ground, arrows) and applies the necessary transformations to display them correctly on screen.

Game

The Game class at the highest level, and is a kind of supervisor. It is mainly responsible for generating the infinite game loop and responding to player events.