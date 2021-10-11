import math

i = 0 + 1j
def xi(z):
    return (i * z + 1) / (- z - i)

# Möbiustranform, mapping line of D to line in H and then to imaginary axis in H
def m(a,b,z):
    ma = max(xi(a).real, xi(b).real)
    mi = min(xi(a).real, xi(b).real)
    return (xi(z) - ma) / (xi(z) - mi)

# the geodesic in the half plane model
def gamma_H(a, b, s, e, t):
    # depending on whether the starting point s is below or above the ending point s, we move upwards or downwards,respectively
    if m(a,b,s).imag < m(a,b,e).imag:
        return m(a,b,s) * (math.e ** t)
    else:
        return m(a,b,s) * (math.e ** (-t))

def m_inv(a,b,z):
    ma = max(xi(a).real, xi(b).real)
    mi = min(xi(a).real, xi(b).real)
    return ((1 + i * mi) * z - 1 - i * ma) / ((-i - mi) * z + i + ma)

def gamma_D(s,e,a,b,t):
    return m_inv(a,b, gamma_H(a, b, s, e, t))