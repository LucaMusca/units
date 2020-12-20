from units.core import Unit, BaseUnit
import numpy as np
import itertools
import functools


@functools.lru_cache(20)
def simplify(u: tuple):
    dim = BaseUnit.dim
    units = Unit.units
    baseUnits = BaseUnit.baseUnits
    allUnits = {**units, **baseUnits}
    for i in range(1, dim + 1):
        for s in itertools.combinations(baseUnits, r=i):
            x, residual, *_ = np.linalg.lstsq(np.column_stack([baseUnits[v].data for v in s]), u, rcond=None)
            if residual[0] < 1e-4:
                return {s[k]: int(v) if abs(v - np.floor(v)) < 1e-4 else v for k, v in enumerate(x) if abs(v) > 1e-4}
        for n in range(1, i + 1):
            for b in itertools.combinations(baseUnits, r=i - n):
                for s in itertools.combinations(units, r=n):
                    union = s+b
                    x, residual, *_ = np.linalg.lstsq(np.column_stack([allUnits[v].data for v in union]), u, rcond=None)
                    if len(residual) and residual[0] < 1e-4:
                        return {union[k]: np.round(v,3) for k, v in enumerate(x) if
                                abs(v) > 1e-4}
