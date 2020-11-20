"""Definition of PREPEND."""

from colorama import init
from colorama import Fore, Style

init()


def PREPEND(state):
    """PREPEND is used to print ==> in front of the lines.
    They are colorised according to their status.
    If everything is good then green else red.
    """
    # State 1 is for ok
    # State 2 is for notok

    print(Style.BRIGHT, end='')
    if state == 1:
        print(Fore.LIGHTGREEN_EX, end='')
    elif state == 2:
        print(Fore.LIGHTRED_EX, end='')
    else:
        pass

    print(' ==> ', end='')
    print(Style.RESET_ALL, end='')