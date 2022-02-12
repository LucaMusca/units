from units.SI_units import *
import units.math as math

pi = math.pi

G = 6.67408e-11 * m ** 3 * kg ** -1 * s ** -2
h = 6.62607004e-34 * J * s
hb = h / (2*pi)

c = 299_792_458 * m / s
e = 1.60217662e-19 * C
m_el = 9.1093837015e-31 * kg  # mass of the electron
m_pr = 1.67262e-27 * kg   # mass of the proton
eps0 = 8.8541878128e-12 * F / m
mu0 = 1.25663706212e-6 * H / m
k0 = 1/(4*math.pi*eps0)

kB = 1.38064852e-23 * J / K
nA = 6.0221409e+23 / mol
stef_bolt = 5.670374419e-8 * W / (m**2 * K**4)

g = 9.81 * m / s**2
Z_0 = math.sqrt(mu0/eps0)
