from units.core import Quantity, Unit
import math
from math import *


def sqrt(x):
    if isinstance(x, Quantity) or isinstance(x, Unit):
        return x ** (1 / 2)
    else:
        return math.sqrt(x)


def __getattribute__(item):
    if item in ['sqrt']:
        return locals()[item]
    return getattr(math, item)
