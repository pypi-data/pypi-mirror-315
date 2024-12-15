"""
https://github.com/kokaito-git/kcolors
Automátic ANSI colors for Python Scripts. This script also enables Virtual Terminal (VT) mode to support ANSI escape
sequences by configuring the console mode using the `ctypes` library.

The value of the dynamic class Colors will be "" if output is not a terminal:
  - `python program.py > file.txt` (no colors)
  - `python program.py | cat` (no colors)
  - `python program.py` (colors, but only if executed from a terminal)

Classes:
- **Colors**: Dynamic Colors. Provides dynamic color codes and text formatting that adapt based on whether the output
 is to a terminal.
- **SColors**: Static Colors. Provides the same colors, but they will always be printed, where doesn't matter.

Attributes (both `Colors` and `StaticColors`):
- Regular colors: `BLACK`, `RED`, `GREEN`, `YELLOW`, `BLUE`, `PURPLE`, `CYAN`, `GRAY`
- Bold (bright) colors: `BBLACK`, `BRED`, `BGREEN`, `BYELLOW`, `BBLUE`, `BPURPLE`, `BCYAN`, `BGRAY`
- Text formatting options: `BOLD`, `FAINT`, `ITALIC`, `UNDERLINE`, `BLINK`, `NEGATIVE`, `CROSSED`
- `END`: Resets all formatting and colors.

Modules:
- **kcolors.utils**: Utility functions related to ANSI escape codes and terminal support:
  - `remove_ansi_codes(text: str)`: Removes all ANSI escape codes from a string.
  - `remove_color_codes(text: str)`: Removes only ANSI color codes from a string.
  - `win_ensure_vtmode()`: Enables Virtual Terminal (VT) mode on Windows for proper ANSI support.

Usage:
# Access to members
- Import Colors or SColors and access their attributes. For example:
    ```python
    from kcolors import Colors, SColors
    print(Colors.RED + "This text is red." + Colors.END)
    print(SColors.RED + "This text is red." + SColors.END)
    ```

# Use references
## Create your own references
You can create your own color references. This is an example:
  - https://github.com/kokaito-git/kcolors/blob/main/kcolors/samples/colors.py

## Use our kcolors references
### Preferred Methods
#### References ({BLACK} is dynamic, {BLACK_} is static)
from kcolors.refs import BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, GRAY, BBLACK, BRED, BGREEN, BYELLOW, BBLUE, \
 BPURPLE, BCYAN, BGRAY, END, BLACK_, RED_, GREEN_, YELLOW_, BLUE_, PURPLE_, CYAN_, GRAY_, BBLACK_, BRED_, BGREEN_, \
 BYELLOW_, BBLUE_, BPURPLE_, BCYAN_, BGRAY_, END_

#### Inverse references ({BLACK} is static, {BLACK_} is dynamic)
from kcolors.irefs import BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, GRAY, BBLACK, BRED, BGREEN, BYELLOW, BBLUE, \
 BPURPLE, BCYAN, BGRAY, END, BLACK_, RED_, GREEN_, YELLOW_, BLUE_, PURPLE_, CYAN_, GRAY_, BBLACK_, BRED_, BGREEN_, \
  BYELLOW_, BBLUE_, BPURPLE_, BCYAN_, BGRAY_, END_

### Not Recommended (but simpler)
from kcolors.refs import * # pyright: ignore
from kcolors.irefs import * # pyright: ignore
"""
from .src.colors import SColors, Colors
