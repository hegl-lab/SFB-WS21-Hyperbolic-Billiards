from h2geometry import *

class Polygon:
    def __init__(self, nr, vertices):
        self.nr = nr
        self.vertices = vertices
    
    def reflect(polygon, s):
        '''It reflects a polygon across a given geodesic s and returns the new polygon'''
        new_vertices = []
        for vertex in self.vertices:
            ref = s.reflect(vertex)
            new_vertices.append(ref)
        return Polygon(self.nr, new_vertices)
