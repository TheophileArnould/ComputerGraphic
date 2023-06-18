import numpy as np

class Player:

    def __init__(self, position):
        self.position = np.array(position, dtype = np.float32)
        self.theta = 0 #front, back, sides
        self.phi = 0 #up and down
        self.update_vectors()
    
    def update_vectors(self):
        
        self.forwards = np.array(
            [
                np.cos(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)), #spherical coordonnates
                np.sin(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.phi))
            ]
        )

        globalUp = np.array([0,0,1], dtype=np.float32)

        self.right = np.cross(self.forwards, globalUp)

        self.up = np.cross(self.right, self.forwards)

        self.rotate = np.array([self.phi*np.sin(self.theta),self.phi,self.theta])# x angle y angle and z angle
    '''
    def direction_to_euler(self,direction):
        # Normalize the direction vector
        direction_normalized = direction / np.linalg.norm(direction)

        # Calculate pitch angle
        pitch = np.arcsin(-direction_normalized[1])

        # Calculate yaw angle
        yaw = np.arctan2(direction_normalized[0], direction_normalized[2])

        # Set roll angle to 0
        roll = 0

        # Convert angles from radians to degrees
        pitch_deg = np.rad2deg(pitch)
        yaw_deg = np.rad2deg(yaw)
        roll_deg = np.rad2deg(roll)

        return pitch_deg,yaw_deg, yaw_deg
    '''
        