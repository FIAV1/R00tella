#!/usr/bin/env python

""" Utils module used to print coloured messages onto the shell (improved user experience) """

DEFAULTBG = '\033[49m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINED = '\033[4m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[31m'
ORANGE = '\033[91m'


# Use this color for ERRORS
def print_red(string, end='\n'):
    print(DEFAULTBG + BOLD + RED + string + RESET, end=end)


# Use this color for INFO
def print_blue(string, end='\n'):
    print(DEFAULTBG + BOLD + BLUE + string + RESET, end=end)


# Use this color for SUCCESS
def print_green(string, end='\n'):
    print(DEFAULTBG + BOLD + GREEN + string + RESET, end=end)


# Use this color for WARNINGS
def print_yellow(string, end='\n'):
    print(DEFAULTBG + BOLD + YELLOW + string + RESET, end=end)


# Use this color for PROGRESSING ACTIONS
def print_orange(string, end='\n'):
    print(DEFAULTBG + BOLD + ORANGE + string + RESET, end=end)
