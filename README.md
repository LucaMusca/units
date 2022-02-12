# units
I developed this package to perform simple physics computations in the Python interactive shell. *More magic is available when IPython is used*.
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

When the extension is loaded in IPython, putting multiplication sign ('*') between units and quantities is not necessary anymore. Furthermore, the caret sign('^') can be used instead of '**'. The system will now not allow variable names already bound to units to be written.
```Python
%load_ext units
>>> Unit calculation and physics extensions activated.

10 kg m^-3
>>> 10 kg m^-3

2e-32 hb c
>>> 6.32e-58 N m^2

T = 12
>>> UserWarning: You are trying to overwrite "protected" name T, reserved for units.
Instead, I gave name T0 to it.

T0, T
>>> 12, T
```
