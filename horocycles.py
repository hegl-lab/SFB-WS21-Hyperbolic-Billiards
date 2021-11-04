from h2geometry import H2_segment, H2_reflection
from math import sqrt
from tools import normsq

class Horocycle:
    def __init__(self, euclRadius, tanPoint):
        self.euclRadius = euclRadius
        self.tanPoint = tanPoint
    
    def euclCenter(self):
        return (1 - self.euclRadius) * self.tanPoint

    def closestAndFurthest(self, s):
        #we only need c
        radius, c = s.get_circle()
        if radius != -1:
            hCenter = self.euclCenter()
            return hCenter + self.euclRadius * (c - hCenter) / sqrt(normsq(c - hCenter)), hCenter - self.euclRadius * (c - hCenter) / sqrt(normsq(c - hCenter))
        return self.tanPoint, self.tanPoint
    
    def reflect_horocycle(self, s):
        #assume s is not a diameter for the moment
        #get closest anf furthest points from s
        z1, z2 = self.closestAndFurthest(s)
        if z1 != z2:
            #reflect the points
            z1_ref = H2_reflection(s).reflect(z1)
            z2_ref = H2_reflection(s).reflect(z2)
            #reflect self.tanPoint
            tanPoint_ref = H2_reflection(s).reflect(self.tanPoint)
            #z1_ref and z2_ref will also be diametrically opposed on the new horocycle
            #find the radius using them
            newRadius = sqrt(normsq(z2_ref - z1_ref)) / 2
            #return a new Horocycle object
            return Horocycle(newRadius, tanPoint_ref)
        else:
            tanPoint_ref = H2_reflection(s).reflect(self.tanPoint)
            return Horocycle(self.euclRadius, tanPoint_ref)



