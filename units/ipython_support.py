import re
import tokenize
import warnings
from typing import List

from IPython.core.inputtransformer2 import _find_assign_op

from units.core import Unit, BaseUnit
import keyword
from IPython.core import inputtransformer2

"""number = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE]+[+-]?\d+)?)"  # doesn't match complex numbers


unitBasePattern = "\w+"  # "|".join(allUnits)
unitRaisedPattern = fr"(?:{unitBasePattern})(?:\s*\^\s*-?\d+)?"
unitFullPattern = fr"((?:{unitRaisedPattern})(?:\s+(?:{unitRaisedPattern}))*)"
quantity = re.compile(fr"\b(?:{number}\s+)?{unitFullPattern}\b")


def transform(line):
    builder = []
    while m := quantity.search(line):
        start, stop = m.span()
        builder.append(line[:start])
        result = []
        if m.group(1):
            result.append(m.group(1))  # number
        tmp = []
        for unitMatch in re.compile(f'({unitRaisedPattern})').finditer(m.group(2)):
            if m.group(2)[unitMatch.start():unitMatch.end()] in keyword.kwlist:
                builder.append(line[start:stop])
                line = line[stop:]
                break
            tmp.append(f"{unitMatch.group(1).replace('^', '**')}")
        result.append(" * ".join(tmp))
        builder.extend(result)
        line = line[stop:]

    builder.append(line)
    return ''.join(builder)


def input_transformer(lines):
    return [transform(l) for l in lines]"""


def load_ipython_extension(ipython):
    ipython.input_transformer_manager.token_transformers.append(TransformBase)
    print('Unit calculation and physics extensions activated.')


class TransformBase(inputtransformer2.TokenTransformBase):
    allUnits = {**Unit.units, **BaseUnit.baseUnits}

    def __init__(self, start, style, end=None):
        self.end = end[1] if end else None
        self.style = style
        super().__init__(start)

    @classmethod
    def find(cls, tokens_by_line):
        # change "a b" into "a * b"
        for line in tokens_by_line:
            for i in range(len(line) - 1):
                t1, t2 = line[i], line[i + 1]
                if (t1.type in (tokenize.NAME, tokenize.NUMBER) and t2.type == tokenize.NAME and
                        t1.string not in keyword.kwlist and t2.string not in keyword.kwlist):
                    return cls(line[i + 1].start, "NAMES")

        # change "a ^ 2" into "a ** 2"
        for line in tokens_by_line:
            for i in range(len(line) - 2):
                t1, t2, t3 = line[i], line[i + 1], line[i + 2]
                if t2.string == "^":
                    if t1.type == tokenize.NAME and t3.type == tokenize.NUMBER:
                        return cls(line[i + 1].start, "CARET")

        # prevent from assigning to units
        for line in tokens_by_line:
            assign_ix = _find_assign_op(line)
            if assign_ix is not None and line[assign_ix - 1].string in cls.allUnits:
                return cls(line[assign_ix - 1].start, "ASSIGNMENT", line[assign_ix - 1].end)

    def transform(self, lines: List[str]):
        """Transform a magic assignment found by the ``find()`` classmethod.
        """
        start_line, start_col = self.start_line, self.start_col
        end_line = inputtransformer2.find_end_of_continued_line(lines, start_line)
        lines_before = lines[:start_line]
        lines_after = lines[end_line + 1:]

        line = lines[start_line]

        if self.style == "NAMES":
            new_line = line[:start_col] + "* " + line[start_col:]
            return lines_before + [new_line] + lines_after

        elif self.style == "CARET":
            new_line = line[:start_col] + "** " + line[start_col + 1:]
            return lines_before + [new_line] + lines_after
        else:  # style is "ASSIGNMENT"
            string = line[start_col:self.end]
            i = 0
            while True:
                if f"{string}{i}" not in globals():
                    new_string = f"{string}{i}"
                    break
                i += 1
            warnings.warn(f'You are trying to overwrite "protected" name {string}, reserved for units.\n'
                          f'Instead, I gave name {new_string} to it''')
            new_line = line[:start_col] + new_string + line[self.end:]
            return lines_before + [new_line] + lines_after
