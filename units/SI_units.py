from units.core import BaseUnit, Unit

kg = BaseUnit('kg', 0)
m = BaseUnit('m', 2)
s = BaseUnit('s', 1)
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
T = Unit(kg / s ** 2 / A, label='T')
H = Unit(Ohm * s, label='H')

Hz = 1/s
cm = m/100
km = 1000 * m
eV = 1.60217662e-19 * J
