from tools import *
import numpy as np
import math

class H2_segment:
    ''' This class implements a hyperbolic segment or geodesic in the Poincaré disk model '''

    def __init__(self, z1, z2):
        if math.sqrt(normsq(z1))<= 1.0 + 1e-2 and math.sqrt(normsq(z2)) <= 1.0 + 1e-2:
            self.z1 = z1
            self.z2 = z2
        else:
            self.z1 = 0 + 0j
            self.z2 = self.z1

    def get_circle(self):
        ''' returns the Euclidean circle that the hyperbolic segment is an arc of '''
        x1 = self.z1.real
        y1 = self.z1.imag
        x2 = self.z2.real
        y2 = self.z2.imag
        error = 10 ** (-2)
        if abs(x1 * y2 - x2 * y1) >= error:
            x = (x1**2 * y2 - x2**2 * y1 + y1**2 * y2 - y1 * y2**2 + y2 - y1) / (2 * (x1 * y2 - x2 * y1))
            y = (x1**2 * x2 - x1 * x2**2 + y1**2 * x2 - x1 * y2**2 + x2 - x1) / (2 * (x2 * y1 - x1 * y2))
            c = x + y * 1j
            r = math.sqrt(normsq(self.z1 - c))
            return r, c
        else:
            return -1, 0 + 0j
                                                  
    def get_ideal_endpoints(self):
        ''' returns the ideal endpoints of the geodesic extending the segment '''
        # complete
        r,c = self.get_circle()
        if r == -1 and c == 0 + 0j:
            z1 = self.z1
            z2 = self.z2
            if normsq(z1) == 0:
                z = z2
            else:
                z = z1
            if normsq(z) == 0 or z1 == z2:
                return 0 + 0j, 0 + 0j
            x1 = z.real / math.sqrt(normsq(z))
            x2 = -x1
            y1 = z.imag / math.sqrt(normsq(z))
            y2 = -y1
        else:
            a = c.real
            b = c.imag
            if a != 0:
                y1 = (b + a * r) / (r**2 + 1)
                y2 = (b - a * r) / (r**2 + 1)
                x1 = (1 - b * y1) / a
                x2 = (1 - b * y2) / a
            else:
                y1 = y2 = 1 / b
                x1 = math.sqrt(1 - 1 / b**2)
                x2 = -x1
        e1 = x1 + y1 * 1j
        e2 = x2 + y2 * 1j
        return e1, e2


class H2_reflection:
    def __init__(self, s : H2_segment):
        ''' Initialization '''
        self.s = s

    def reflect(self, z):
        ''' Computes the reflection of a point '''
        r, c = self.s.get_circle()
        #case 1: s is a euclidean circle arc
        if not (r == -1 and c == 0 + 0 * 1j):
            a = c.real
            b = c.imag
            x = z.real
            y = z.imag
            if x == a and y == b:
                x_ref = x
                y_ref = y
            else:
                x_ref = a + (x - a) * r ** 2 / ( (x - a) ** 2 + (y - b) ** 2)
                y_ref = b + (y - b) * r ** 2 / ( (x - a) ** 2 + (y - b) ** 2)
            z_ref = x_ref + y_ref * 1j
            if math.sqrt(normsq(z_ref)) - 1.0 < 1e-1:
                return z_ref
            else:
                return 0 + 0j
        #case 2: s is a diameter
        else:
            x = z.real
            y = z.imag
            e1, e2 = self.s.get_ideal_endpoints()
            if e2.real - e1.real != 0:
                slope = (e2.imag - e1.imag) / (e2.real - e1.real)
                if slope != 0:
                    x_ref = (2 * (y - e1.imag + slope * e1.real) - x * (slope - 1 / slope)) / (slope + 1 / slope)
                    y_ref = (2 * (e1.imag / slope + x - e1.real) + y * (slope - 1 / slope)) / (slope + 1 / slope)
                else:
                    x_ref = x
                    y_ref = -y
            else:
                x_ref = -x
                y_ref = y
            z_ref = x_ref + y_ref * 1j
            if math.sqrt(normsq(z_ref)) < 1.0 + 1e-10:
                return z_ref
            else:
                return 0 + 0j

########################################################
def intersection_points_of_circles(r1, r2, c1, c2):
    x1, y1 = c1.real, c1.imag
    x2, y2 = c2.real, c2.imag
    d12 = math.sqrt(normsq(c2 - c1))
    d0 = ((r1 ** 2) - (r2 ** 2) + (d12 ** 2)) / (2 * d12)
    if (r1 ** 2) - (d0 ** 2) > 0:
        e0 = math.sqrt(r1 ** 2 - d0 ** 2)
        m = (x2 - x1) / d12 + (y2 - y1) / d12 * 1j
        n = (y1 - y2) / d12 + (x2 - x1) / d12 * 1j
        p1 = c1 + d0 * m + e0 * n
        p2 = c1 + d0 * m - e0 * n
        ok = True
    else:
        p1 = p2 = 0 + 0j
        ok = False
    return p1, p2, ok

def intersection_points_line_circle_angle(r, c, z, angle):
    #added the case with angle == +/- 90
    if abs(angle) != 90:
        d = tan(angle) * z.real - z.imag - tan(angle) * c.real + c.imag
        if (r ** 2) * (tan(angle) ** 2 + 1) > d ** 2:
            x1 = c.real + (tan(angle) * d - math.sqrt((r ** 2) * (tan(angle) ** 2 + 1) - (d ** 2))) / (tan(angle) ** 2 + 1)
            x2 = c.real + (tan(angle) * d + math.sqrt((r ** 2) * (tan(angle) ** 2 + 1) - (d ** 2))) / (tan(angle) ** 2 + 1)
            y1 = c.imag + (-d - tan(angle) * math.sqrt((r ** 2) * (tan(angle) ** 2 + 1) - d ** 2)) / (tan(angle) ** 2 + 1)
            y2 = c.imag + (-d + tan(angle) * math.sqrt((r ** 2) * (tan(angle) ** 2 + 1) - d ** 2)) / (tan(angle) ** 2 + 1)
            p1 = x1 + y1 * 1j
            p2 = x2 + y2 * 1j
            ok = True
        else:
            p1 = p2 = 0 + 0j
            ok = False
    else:
        if r ** 2 - (z.real - c.real) ** 2 >= 0:
            p1 = z.real + (c.imag + math.sqrt(r ** 2 - (z.real - c.real) ** 2)) * 1j
            p2 = z.real + (c.imag - math.sqrt(r ** 2 - (z.real - c.real) ** 2)) * 1j
            ok = True
        else:
            p1 = p2 = 0 + 0j
            ok = False
    return p1, p2, ok


def intersection_points_line_circle(r, c, a, b):
    if a.real == b.real:
        #corrected the condition here
        if r ** 2 - (a.real - c.real) ** 2 < 0:
            p1 = p2 = 0 + 0j
            ok = False
        else:
            #corrected the formulas here
            p1 = a.real + (c.imag + math.sqrt((r ** 2) - (a.real - c.real) ** 2)) * 1j
            p2 = a.real + (c.imag - math.sqrt((r ** 2) - (a.real - c.real) ** 2)) * 1j
            ok = True
    else:
        m  = (b.imag - a.imag) / (b.real - a.real)
        # instead of m * c.real - c.imag it must be m * a.real - a.imag
        d = m * a.real - a.imag - m * c.real + c.imag
        if (r ** 2) * ((m ** 2) + 1) > d ** 2:
            x1 = c.real + (m * d - math.sqrt(r ** 2 * (m ** 2 + 1) - d ** 2)) / (m ** 2 + 1)
            x2 = c.real + (m * d + math.sqrt(r ** 2 * (m ** 2 + 1) - d ** 2)) / (m ** 2 + 1)
            y1 = c.imag + (-d - m * math.sqrt(r ** 2 * (m ** 2 + 1) - d ** 2)) / (m ** 2 + 1)
            y2 = c.imag + (-d + m * math.sqrt(r ** 2 * (m ** 2 + 1) - d ** 2)) / (m ** 2 + 1)
            p1 = x1 + y1 * 1j
            p2 = x2 + y2 * 1j
            ok = True
        else:
            p1 = p2 = 0 + 0j
            ok = False
    return p1, p2, ok
########################################################

def H2_midpoint(z1, z2):
    ''' Computes the hyperbolic midpoint of two points in the Poincaré disk model '''
    if z1 == z2:
        return z1

    fz2 = H2_midpoint_isometry(z1, z2) #f
    
    #find hyperbolic distance from 0 = f(z1) to f(z2)
    r1 = math.sqrt(normsq(fz2)) #euclidean distance from 0 to f(z2)
    hyp_dist = hyp_dist_from_eucl_dist(r1)
    
    #find midpoint between f(z1) and f(z2)
    half_hyp_dist = hyp_dist / 2
    r2 = eucl_dist_from_hyp_dist(half_hyp_dist)
    fm = r2 / r1 * fz2

    return H2_midpoint_inverse_isometry(z1, fm)

def H2_midpoint_isometry(z1, z):
    """Sends z1 to 0 and z somewhere else."""
    return (z - z1) / (1 - np.conj(z1) * z)

def H2_midpoint_inverse_isometry(z1, z):
    """Sends 0 to z1. This is the inverse of H2_midpoint_isometry."""
    return (z + z1) / (1 + np.conj(z1)*z)

def hyp_dist_from_eucl_dist(r):
    """Returns the hyperbolic distance between 0 and some point with euclidean distance r."""
    return math.log((1 + r) / (1 - r))

def eucl_dist_from_hyp_dist(h):
    """Returns the euclidean distance that gives the hyperbolic distance h.
    This only works when one point is at 0."""
    return (-1 + math.exp(h)) / (1 + math.exp(h))  

def iso_map(z,a):
    ''' Computes an isometry '''
    q = a.conjugate()
    print(q,z)
    r = (z-a)/(1-q*z)
    return r

def get_angle(z1,z2,z12,z22):
    ''' Gives you the smallest angle between two line segments defined by points'''
    a = iso_map(z1,z1)
    b = iso_map(z2,z1)
    c = iso_map(z12,z12)
    d = iso_map(z22,z12)
    slope1 = (a.real - b.real) / (b.imag - a.imag)
    print(slope1)
    slope2 = (c.real - d.real) / (d.imag - c.imag)
    
    tan_alpha = abs((slope1 - slope2)/(1 + slope1 * slope2))
    #changed np.atan in arctan, maybe its an tan i dont know?
    rad_angle = np.arctan(tan_alpha)
    if(rad_angle > (np.pi/2)):
        return np.pi - rad_angle
    else:
#       <<<<<<< HEAD
        return rad_angle






