from units.core import BaseUnit, Unit


kg = BaseUnit('kg', 0)
s = BaseUnit('s', 1)
m = BaseUnit('m', 2)
A = BaseUnit('A', 3)
K = BaseUnit('K', 4)
cd = BaseUnit('cd', 5)
mol = BaseUnit('mol', 6)

N = Unit(kg * m / s ** 2, label='N')
J = Unit(N * m, label='J')
W = Unit(J / s, label='W')

C = Unit(A * s, label='C')
V = Unit(J / C, label='V')
Ohm = Unit(V / A, label='Ohm')
F = Unit(C / V, label='F')
T = Unit(V * s, label='T')
H = Unit(Ohm * s, label='H')
Pa = Unit(N/m**2,label='Pa')

Hz = 1/s
cm = m/100
km = 1000 * m
eV = 1.60217662e-19 * J
kph = 1/3.6 * m / s  # km per hour
u = 10e-3 * kg / mol  # atomic unit mass
