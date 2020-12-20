# units
I developed this package to perform simple physics computations in the Python interactive shell.
# Examples of usage
Import the module
```Python
import units
from units.SI_units import *
from units.constants import *
```
You have now the most common SI units and physical constants loaded in the console. You can create quantities by simply multiplying together other quantities, units, or numbers.
```Python
r = 6371e3 * m
r ** 2
>>> 4.06e+13 m^2
m1,m2 = 1 * kg, 5.97e24 * kg
m1*m2*G/r**2
>>> 9.82 N
_.value
>>> 9.81636117451741
mu0
>>> 1.26e-06 H m^-1
```
Quantities are displayed using the least possible number of named units. You can create new named units as in the following example.
```Python
a = 10 * kg / m**3
a
>>> 10 kg m^-3
density = units.Unit(kg / m**3,label='density')
a
>>> 10 density
```
