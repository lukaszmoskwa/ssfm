# coding=utf-8

import curses
import sys
from importlib import reload
import locale
locale.setlocale(locale.LC_ALL, '')
reload(sys)
# Function used to draw


def draw_file(main_win, isSelected):
    """Function used to draw the file"""
    pos = main_win.pos_idx
    dim = main_win.file_dimension
    for y in range(0, dim["y"]-1):
        for x in range(0, dim["x"]):
            if y == 0:
                main_win.outwin.addstr(pos["y"] + y, pos["x"] + x, "┏" if x == 0 else (
                    "┓" if x == dim["x"]-1 else "━"), curses.A_NORMAL if isSelected else curses.A_REVERSE)
            elif y == dim["y"]-2:
                main_win.outwin.addstr(pos["y"] + y, pos["x"] + x, "┗" if x == 0 else (
                    "┛" if x == dim["x"]-1 else "━"), curses.A_NORMAL if isSelected else curses.A_REVERSE)
            else:
                main_win.outwin.addstr(pos["y"] + y, pos["x"] + x, "┃" if x == 0 or x ==
                                       dim["x"]-1 else "-", curses.A_NORMAL if isSelected else curses.A_REVERSE)


def draw_folder(main_win, isSelected):
    """Function used to draw the folder"""
    pos = main_win.pos_idx
    dim = main_win.file_dimension
    up_dir = "┏━━┓"
    up_dir = up_dir.encode("utf-8", "ignore").decode("utf-8")
    main_win.outwin.addstr(pos["y"], pos["x"]+dim["x"]-4, up_dir,
                           curses.A_NORMAL if isSelected else curses.A_REVERSE)
    for y in range(1, dim["y"]-1):
        for x in range(0, dim["x"]):
            if y == 1:
                main_win.outwin.addstr(pos["y"] + y, pos["x"] + x, "┏" if x == 0 else ("┃" if x == dim["x"]-1 else (
                    "┛" if x == dim["x"]-4 else "━")),  curses.A_NORMAL if isSelected else curses.A_REVERSE)
            elif y == dim["y"]-2:
                main_win.outwin.addstr(pos["y"] + y, pos["x"] + x, "┗" if x == 0 else (
                    "┛" if x == dim["x"]-1 else "━"),  curses.A_NORMAL if isSelected else curses.A_REVERSE)
            else:
                main_win.outwin.addstr(pos["y"] + y, pos["x"] + x, "┃" if x == 0 or x ==
                                       dim["x"]-1 else " ", curses.A_NORMAL if isSelected else curses.A_REVERSE)
