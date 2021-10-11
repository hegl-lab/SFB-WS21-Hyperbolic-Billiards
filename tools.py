#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import math

def mod2pi(t):
    q= int(t/(2*np.pi))
    if t<0:
        q -= 1
    return t - 2*np.pi*q
    
def normsq(z):
    return z.real*z.real + z.imag*z.imag

sin = lambda degs: math.sin(math.radians(degs))
cos = lambda degs: math.cos(math.radians(degs))
tan = lambda degs: sin(degs) / cos(degs)
arctan = lambda degs: math.atan(math.radians(degs))
arcsin = lambda degs: math.asin(math.radians(degs))