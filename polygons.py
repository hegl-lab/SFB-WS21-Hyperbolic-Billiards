from h2geometry import H2_reflection
import math
import numpy as np

class Polygon:
    def __init__(self, nr, angles):
        self.nr = nr
        self.angles = angles
    
    def reflect(self, s):
        '''It reflects a polygon across a given geodesic s and returns the new polygon'''
        new_angles = []
        for angle in self.angles:
            vertex = math.e ** (angle * 1j)
            ref = H2_reflection(s).reflect(vertex)
            new_ang = np.angle(ref)
            new_angles.append(new_ang)
        return Polygon(self.nr, new_angles)

