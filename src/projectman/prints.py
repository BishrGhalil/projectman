import sys
import traceback

from colorama import Fore, Style, init

init(autoreset=True)

INFO_FORE = Fore.BLUE
WARN_FORE = Fore.YELLOW
ERROR_FORE = Fore.RED

_pyprint = print


def cstr(string: str, color=Style.RESET_ALL, style=Style.RESET_ALL, reset=True):
    color = {
        "red": Fore.RED,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "green": Fore.GREEN,
        "black": Fore.BLACK,
        "cyan": Fore.CYAN,
    }.get(color.lower(), color)
    style = {
        "bold": Style.BRIGHT,
        "dim": Style.DIM,
        "normal": Style.NORMAL,
    }.get(style.lower(), style)
    s = style + color + str(string)
    if reset:
        s += Style.RESET_ALL
    return s


def print(
    *values,
    sep=" ",
    end="\n",
    file=sys.stdout,
    flush=False,
    color=Style.RESET_ALL,
    style=Style.RESET_ALL
):
    values = list(map(str, values))
    for i in range(len(values)):
        values[i] = cstr(values[i], style=style, color=color, reset=False)
    values[-1] = str(values[-1]) + Style.RESET_ALL
    _pyprint(*values, sep=sep, end=end, file=file, flush=flush)


def info(*values, sep="", end="\n", file=sys.stdout, flush=False):
    print(
        *values,
        sep=sep,
        end=end,
        file=file,
        flush=flush,
        color=INFO_FORE,
        style=Style.BRIGHT
    )


def warn(*values, sep="", end="\n", file=sys.stdout, flush=False):
    print(
        *values,
        sep=sep,
        end=end,
        file=file,
        flush=flush,
        color=WARN_FORE,
        style=Style.BRIGHT
    )


def error(*values, sep="", end="\n", file=sys.stdout, flush=False):
    print(
        *values,
        sep=sep,
        end=end,
        file=file,
        flush=flush,
        color=ERROR_FORE,
        style=Style.BRIGHT
    )


def exception(exc, sep="", end="\n", file=sys.stdout, flush=False):
    tr = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    error(tr)
