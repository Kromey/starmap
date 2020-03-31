import math
import numpy as np


class Projection:
    def __init__(self, size, scale, rotation_x=0, rotation_z=90):
        self.__size = size
        self.__scale = scale

        self.__rotation = {}

        self.set_rotation(x=rotation_x, z=rotation_z)

    def set_rotation(self, *, x=None, z=None):
        if x is not None:
            angle = math.radians(x)
            self.__rotation['x'] = np.array([
                [1, 0, 0],
                [0, math.cos(angle), -math.sin(angle)],
                [0, math.sin(angle), math.cos(angle)],
            ])

        if z is not None:
            angle = math.radians(z)
            self.__rotation['z'] = np.array([
                [math.cos(angle), -math.sin(angle), 0],
                [math.sin(angle), math.cos(angle), 0],
                [0, 0, 1],
            ])

    def ellipse(self, p1, p2):
        #TODO? We're assuming an ellipse parallel to the x-y plane
        p1, p2 = self.points([p1,p2], skip_z=True)

        return p1, p2

    def points(self, points, skip_z=False):
        return [self.point(*point, skip_z=skip_z) for point in points]

    def point(self, x, y, z=0, skip_z=False):
        # Ensure proper types for our input
        coords = np.array([
            float(x),
            float(y),
            # Not sure why, but we need to invert z here to get galactic north/south
            # to show up properly at the top/bottom of the image
            float(-z),
        ])

        if not skip_z:
            # Rotation around z-axis
            coords = np.matmul(coords, self.__rotation['z'])

        ## Rotation around x-axis
        coords = np.matmul(coords, self.__rotation['x'])

        ## DROP Z HERE
        ## This is where z stops mattering for our 2D projection

        # Translate origin to upper left of image
        px = self.__size[0]/2 + coords[0]
        py = self.__size[1]/2 + coords[1]

        # Scale
        px = px * self.__scale
        py = py * self.__scale

        # Round
        px = round(px)
        py = round(py)

        return px, py

