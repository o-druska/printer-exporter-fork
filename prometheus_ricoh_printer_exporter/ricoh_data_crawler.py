# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

# This will be the script that yields the needed information and "talks" to the printers
import re
from dataclasses import dataclass


@dataclass
class Printer_Values:
    '''contains all printer values such as name and toner levels'''

    printer_name: str
    level_black: float
    level_cyan: float
    level_magenta: float
    level_yellow: float


def get_fill_percent(tag) -> float:
    '''
    takes the amount of graphical elements displaying the toner level
    and calculates a percentage.
    160 units make up 100% <=> one unit is 0,625% (constant values)
    '''

    # Toner level needs to be parsed by examining the amount of graphical elements
    # 160 units display 100%, therefore one unit represents 0,625% off toner (100%/160 == 0,635%)
    SINGLE_GRAPHIC_CONSTANT = 100 / 160

    # tag['width'] is the amount of graphic units (s.a.) displayed
    fill_percent = float(tag['width']) * SINGLE_GRAPHIC_CONSTANT
    return fill_percent


def get_printer_values(soups: list, urls: list):
    '''
    gets a list of soups and parses the toner levels for each.
    returns a generator, providing a Printer_Values object in each iteration for each printer URL
    '''

    for (soup, url) in zip(soups, urls):
        tag_list = soup.find_all("img", class_="ver-algn-m mgn-R5p bdr-1px-666", attrs='width')  # html-tags related to toner levels

        yield Printer_Values(
            # url is a tuple containing the name and url itself. url[0] therefore holds the name of the printer
            printer_name=url[0],
            level_black=float(get_fill_percent(tag_list[0])),
            level_cyan=float(get_fill_percent(tag_list[1])),
            level_magenta=float(get_fill_percent(tag_list[2])),
            level_yellow=float(get_fill_percent(tag_list[3]))
        )
