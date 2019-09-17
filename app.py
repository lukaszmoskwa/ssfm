# coding=utf-8

import curses
import os
import sys
from os.path import isfile, join
from math import ceil, floor
from modules.draw_mod import draw_file, draw_folder
from modules.create_file import *


class WindowFileManager:
    outwin = ""
    currentDirectory = ""
    hide_hidden_files = True
    theme_number = 13
    onlydirs = []
    onlyfiles = []
    file_dimension = {
        "x": 8,
        "y": 5
    }
    pos_idx = {
        "x": 1,
        "y": 4
    }
    selected_filename = ".."  # FIX THIS
    selected_index = []
    height = 0
    width = 0
    inserted_word = ""
    test = ""

    def __init__(self):
        if len(sys.argv) > 1 and sys.argv[1] == ".":
            self.currentDirectory = os.getcwd()
        else:
            os.chdir(os.path.expandvars("$HOME"))
            self.currentDirectory = os.getcwd()
        self.create()
        self.run_loop()

    def create(self):
        """Function used to create the screen"""
        self.outwin = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.outwin.keypad(1)
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            for i in range(0, curses.COLORS):
                curses.init_pair(i + 1, i, -1)
        self.height, self.width = self.outwin.getmaxyx()
        self.outwin.box()
        self.outwin.addstr(0, 0, '@'*56, curses.A_REVERSE)
        try:
            self.run_ls()
            self.run_draw()
        except:
            self.currentDirectory = "/"
            self.create()

    def add_file_to_screen(self, filename, isDir, isSelected):
        """Function to add a folder or a file to the screen"""
        pos = self.pos_idx
        dim = self.file_dimension
        if self.pos_idx["x"] + dim["x"] > self.width-1:
            pos["x"] = 1
            pos["y"] += dim["y"] + 1
        if pos["y"] + dim["y"] + 1 < self.height:
            if isDir:
                draw_folder(self, isSelected, self.theme_number)
            else:
                draw_file(self, isSelected, self.theme_number)
            # Add file name TODO Aggiungere in draw_mod
            #floor((dim["x"] - len(filename))/2)
            self.outwin.addstr(pos["y"]+dim["y"] - 1, pos["x"] + floor((dim["x"] - len(filename[:dim["x"]]))/2), filename[:dim["x"]],
                               curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(
                                   self.theme_number)
                               if isDir else
                               curses.color_pair(self.theme_number))
        self.pos_idx["x"] += dim["x"] + 1

    def run_ls(self):
        """Function used to run the ls command in the current directory and call the add_file_to_screen"""
        self.onlyfiles = [f for f in os.listdir(
            self.currentDirectory) if isfile(join(self.currentDirectory, f))]
        self.onlydirs = [f for f in os.listdir(
            self.currentDirectory) if not isfile(join(self.currentDirectory, f))]

    def run_draw(self):
        self.pos_idx = {
            "x": 1,
            "y": 2
        }
        self.outwin.clear()
        self.outwin.addstr(0, 0, '░'*self.width, curses.A_REVERSE |
                           curses.color_pair(self.theme_number))
        self.outwin.addstr(0, 0, self.currentDirectory,
                           curses.A_REVERSE | curses.color_pair(self.theme_number))
        # FILTER FOR HIDDEN FILES
        if self.hide_hidden_files:
            self.onlydirs = list(
                filter(lambda name: name[0] != '.', self.onlydirs))
            self.onlyfiles = list(
                filter(lambda name: name[0] != '.', self.onlyfiles))

        self.files_on_screen = len(self.onlydirs) + len(self.onlyfiles)
        self.BOTTOM = ceil(self.files_on_screen / (self.width //
                                                   self.file_dimension["x"] + 1)) * (self.file_dimension["y"] + 1)
        for el in self.onlydirs:
            self.add_file_to_screen(el, True, el != self.selected_filename)
        for el in self.onlyfiles:
            self.add_file_to_screen(el, False, el != self.selected_filename)

    def display_window(self):
        """Functin used to update the window and refresh the screen on resize"""
        self.outwin.clear()
        self.outwin.refresh()
        self.create()

    def navigate_path(self, path):
        """Function to change the currentDirectory path and create the window again"""
        self.outwin.erase()
        os.chdir(path)
        self.currentDirectory = os.getcwd()
        self.reset_input()
        self.run_ls()
        self.run_draw()

    def navigate_back(self):
        self.outwin.erase()
        os.chdir("..")
        self.currentDirectory = os.getcwd()
        self.reset_input()
        self.run_ls()
        self.run_draw()

    def reset_input(self):
        self.inserted_word = ""
        self.selected_filename = ".."

    def run_loop(self):
        while True:
            try:
                # if self.inserted_word != "":
                self.outwin.addstr(self.height-1, 1, str(self.test))
                #self.outwin.nodelay(1)
                key = self.outwin.getch()
                self.get_input_key(key)
            except KeyboardInterrupt:
                curses.nocbreak()
                curses.echo()
                curses.curs_set(1)
                curses.endwin()
                quit()

    def update_selection(self):
        all_files = self.onlydirs + self.onlyfiles
        for (i, x) in enumerate(all_files):
            if x.lower().find(self.inserted_word.lower()) == 0:
                self.selected_filename = x
                self.selected_index = [i]
                self.test = self.selected_filename
                break
        self.run_draw()

    def arrow_navigate(self, direction, hasShift):
        all_files = self.onlydirs + self.onlyfiles
        if self.selected_filename != "..":
            current_index = all_files.index(self.selected_filename)
            if direction == "RIGHT":
                self.selected_filename = all_files[current_index + 1]
            elif direction == "LEFT":
                self.selected_filename = all_files[current_index - 1]
        self.run_draw()

    def get_input_key(self, key):
        """Function that retrieve an input from the user and parse it"""
        self.height, self.width = self.outwin.getmaxyx()
        if key == curses.KEY_ENTER or key == 10:  # ENTER KEY
            if not isfile(self.selected_filename):
                self.navigate_path(self.selected_filename)
                self.create()
            else:
                subprocess.call(["vim", self.selected_filename])
                self.inserted_word = ""
                curses.curs_set(0)
                self.create()
        elif key == curses.KEY_BACKSPACE:  # BACKSPACE KEY
            self.navigate_back()
        elif key == 78:  # N maiuscola
            create_new_file(self.currentDirectory)
            self.run_ls()
        elif key == 77:  # M maiuscola
            create_new_folder(self.currentDirectory)
            self.run_ls()
        elif key == 84:  # T maiuscola
            subprocess.call(["lxterminal"])
            self.run_draw()
        elif key == 71:  # G maiuscola
            subprocess.call(["tig", "status", self.currentDirectory])
            self.run_draw()
        elif key == 72:  # H maiuscola
            self.hide_hidden_files = not self.hide_hidden_files
            self.run_ls()
            self.run_draw()
        elif key == 32:
            show_maintab()
            self.run_draw()
        elif key == 68:
            delete_selected_file(self.selected_filename)
            self.run_ls()
        elif key == curses.KEY_RESIZE:
            self.display_window()
        elif key == 27:  # ESC per resettare
            self.inserted_word = ""
        elif key == curses.KEY_LEFT:
            self.arrow_navigate("LEFT", False)
        elif key == curses.KEY_RIGHT:
            self.arrow_navigate("RIGHT", False)
        elif key == 258 or key == 259:  # Scroll mouse, va sistemato TODO
            self.theme_number = self.theme_number + 1
        else:
            self.inserted_word += str(chr(key))
            self.update_selection()


def main():
    WindowFileManager()


if __name__ == "__main__":
    print(str(sys.argv))
    main()
