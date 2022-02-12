from typing import Union
import numpy as np
import units

# TODO: add IPython repr_latex
# TODO: add use of prefixes in repr


num = Union[float, int, complex]


def _is_num(x):
    return isinstance(x, float) or isinstance(x, int)


class Unit:
    units = {}
    non_metric_units = {}

    def __new__(cls, unit: 'Unit', *args, **kwargs):
        if isinstance(unit, Unit) and not unit:
            return 1
        if isinstance(unit, np.ndarray) and not unit.any():
            return 1
        return object.__new__(cls)

    def __init__(self, unit, label=None):
        self.label = label
        if isinstance(unit, Unit):
            self.data: np.ndarray = unit.data
        elif isinstance(unit, np.ndarray):
            self.data: np.ndarray = unit
        else:
            raise TypeError()
        if label:
            Unit.units[label] = self
            units.tricks.simplify.cache_clear()

    def __call__(self, value):
        return Quantity(value, self)

    def __bool__(self):
        return bool(self.data.any())

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return False
        else:
            return (self.data == other.data).all()

    def __str__(self):
        if self.label:
            return self.label
        elif self.data.any():
            string = ''
            for k, v in units.tricks.simplify(tuple(self.data)).items():
                if abs(v - np.ceil(v)) < 1e-4:
                    string += f'{k} ' if int(v) == 1 else f'{k}^{int(v)} '
                else:
                    string += f'{k}^{v} '
            return string[:-1]
        else:
            return 'NoneUnit'

    def __repr__(self):
        return str(self)

    def inverse(self):
        return Unit(-self.data)

    def __pow__(self, power, modulo=None):
        return Unit(self.data * power)

    def __mul__(self, other):
        if isinstance(other, Unit):
            return Unit(self.data + other.data)
        if isinstance(other, Quantity):
            return other * self
        if _is_num(other):
            return Quantity(other, self)
        raise NotImplemented

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Unit):
            return Unit(self.data - other.data)
        if isinstance(other, Quantity):
            return Quantity(1 / other.value, self / other.unit)
        if _is_num(other):
            return Quantity(1 / other, self)
        raise NotImplemented

    def __rtruediv__(self, other):
        if _is_num(other):
            return Quantity(other, self.inverse())
        raise NotImplemented


class BaseUnit(Unit):
    dim = 7
    array = np.zeros(dim, object)
    baseUnits = {}

    def __init__(self, name: str, index):
        self.name = name
        self.index = index
        super().__init__(np.array([1 if i == index else 0 for i in range(BaseUnit.dim)]))
        BaseUnit.array[index] = self
        BaseUnit.baseUnits[name] = self

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Quantity:
    class _IncompatibleUnits(Exception):
        def __init__(self, a, b):
            super().__init__(f'{a.unit} is not compatible with {b.unit}')

    def __hash__(self) -> int:
        return hash(self.value)

    def __new__(cls, value, unit):
        if value == 1:
            obj = object.__new__(Unit)
            obj.__init__(unit)
            return obj
        if unit == 1:
            return value
        return object.__new__(cls)

    def __init__(self, value: num, unit: Unit):
        super().__init__()
        if not _is_num(value):
            raise TypeError()
        if not isinstance(unit, Unit):
            raise TypeError()
        self.unit: Unit = unit
        self.value: num = value

    def __repr__(self):
        return f'{self.value:.3g} {self.unit}'

    def __str__(self):
        return repr(self)

    def __pow__(self, power: num, modulo=None):
        if _is_num(power):
            return Quantity(self.value ** power, self.unit ** power)
        raise NotImplemented

    def __add__(self, other):
        if isinstance(other, Quantity):
            if self.unit == other.unit:
                return Quantity(self.value + other.value, self.unit)
            else:
                raise Quantity._IncompatibleUnits(self, other)

    def __sub__(self, other):
        if isinstance(other, Quantity):
            if self.unit == other.unit:
                return Quantity(self.value - other.value, self.unit)
            else:
                raise Quantity._IncompatibleUnits(self, other)

    def __mul__(self, other):
        if isinstance(other, Unit):
            return Quantity(self.value, self.unit * other)
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.unit * other.unit)
        if _is_num(other):
            return Quantity(self.value * other, self.unit)
        raise NotImplemented

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Unit):
            return Quantity(self.value, self.unit / other)
        if isinstance(other, Quantity):
            return Quantity(self.value / other.value, self.unit / other.unit)
        if _is_num(other):
            return Quantity(self.value / other, self.unit)
        raise NotImplemented

    def __rtruediv__(self, other):
        if _is_num(other):
            return Quantity(other / self.value, self.unit.inverse())

    def __neg__(self):
        return Quantity(-self.value, self.unit)


if __name__ == '__main__':
    math = units.math
    from units.SI_units import *
