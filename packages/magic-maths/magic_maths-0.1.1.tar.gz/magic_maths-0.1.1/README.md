# magic-math

Magically import evaluated math expressions. Like so:

```py
from magic_math import TEN_TIMES_FIVE_DIVIDED_BY_TWO
from magic_math import FIVE_TIMES_FIVE
from magic_math import TWO_HUNDRED_MINUS_TEN
from magic_math import SIX_HUNDRED_AND_SIXTY_SIX_DIVIDED_BY_TWO_TIMES_EIGHT
from magic_math import OPEN_FIVE_MINUS_THREE_CLOSE_TIMES_TEN

ABC=7
from magic_math import OPEN_TEN_MINUS_OPEN_ABC_DIVIDED_BY_TWO_CLOSE_CLOSE

print(f"{TEN_TIMES_FIVE_DIVIDED_BY_TWO = }")  # 25.0
print(f"{FIVE_TIMES_FIVE = }")  # 25.0
print(f"{TWO_HUNDRED_MINUS_TEN = }")  # 190.0
print(f"{SIX_HUNDRED_AND_SIXTY_SIX_DIVIDED_BY_TWO_TIMES_EIGHT = }")  # 2664.0
print(f"{OPEN_FIVE_MINUS_THREE_CLOSE_TIMES_TEN = }")  # 20.0
print(f"{OPEN_TEN_MINUS_OPEN_ABC_DIVIDED_BY_TWO_CLOSE_CLOSE = }")  # 6.5
```

Notes:

- All returned values are in floating point form
- Floats can be specified using "point" or "dot"
- Variables are partially supported, currently only within scripts
- Uses basic postfix order of precendence
- Basic parenteses syntax using `OPEN` and `CLOSE` values

## Installation

```sh
python3 -m pip install magic-maths
```

Credits:

- Inspired by and uses code from David Buchanan's [`magic-numbers` package](https://github.com/DavidBuchanan314/magic-numbers)