"""
Some utils related with the work that this library does. By now it contains three functions

`remove_ansi_codes(str)`: Removes all ANSI codes using regex and returns the cleaned string.
`remove_color_codes(str)`: Removes ANSI color codes, including BOLD, END, etc.
`win_ensure_vtmode()`: Enables VT mode on Windows for proper ANSI support.
"""

import re


def remove_ansi_codes(text: str) -> str:
    """
    Removes all ANSI escape codes from the given text.
    text (str): Input text with ANSI codes.
    return (str):  Text without ANSI escape codes.
    """
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def remove_color_codes(text: str) -> str:
    """
    Removes ANSI color codes from the given text.
    text (str): Input text with ANSI color codes.
    return (str):  Text without ANSI color codes.
    """
    ansi_escape = re.compile(r"\033\[[0-9;]*m")
    return ansi_escape.sub("", text)


def win_ensure_vtmode():
    """Enable VT mode (for Windows)"""
    if __import__("sys").stdout.isatty():
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32
