# coding=utf-8

import curses
import os
from os.path import isfile, join
from math import ceil
from modules.draw_mod import draw_file, draw_folder
from modules.create_file import *


class WindowFileManager:
    outwin = ""
    currentDirectory = ""
    hide_hidden_files = True
    onlydirs = []
    onlyfiles = []
    file_dimension = {
        "x": 8,
        "y": 5
    }
    pos_idx = {
        "x": 1,
        "y": 1
    }
    selected_filename = ".."  # FIX THIS
    height = 0
    width = 0
    inserted_word = ""
    test = ""

    def __init__(self):
        self.currentDirectory = "/home/lukasz"  # change with default home
        self.create()
        self.run_loop()

    def create(self):
        """Function used to create the screen"""
        self.outwin = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            for i in range(0, curses.COLORS):
                curses.init_pair(i + 1, i, -1)
        self.height, self.width = self.outwin.getmaxyx()
        self.outwin.box()
        try:
            self.run_ls()
        except:
            self.currentDirectory = "/"
            self.create()

    def add_file_to_screen(self, filename, isDir, isSelected):
        """Function to add a folder or a file to the screen"""
        pos = self.pos_idx
        dim = self.file_dimension
        self.pos_idx["x"] += dim["x"] + 1
        if self.pos_idx["x"] + dim["x"] > self.width-1:
            pos["x"] = 1
            pos["y"] += dim["y"] + 1
        if pos["y"] + dim["y"] + 1 < self.height:
            draw_folder(self, isSelected) if isDir else draw_file(
                self, isSelected)  # self.draw_file(isSelected)
            # Add file name TODO Aggiungere in draw_mod
            self.outwin.addstr(pos["y"]+dim["y"] - 1, pos["x"], filename[:dim["x"]],
                               curses.A_BOLD | curses.A_UNDERLINE | curses.color_pair(15)
                               if isDir else
                               curses.color_pair(15))

    def run_ls(self):
        """Function used to run the ls command in the current directory and call the add_file_to_screen"""
        self.outwin.clear()
        self.onlyfiles = [f for f in os.listdir(
            self.currentDirectory) if isfile(join(self.currentDirectory, f))]
        self.onlydirs = [f for f in os.listdir(
            self.currentDirectory) if not isfile(join(self.currentDirectory, f))]
        self.pos_idx = {
            "x": 1,
            "y": 1
        }
        if self.hide_hidden_files:
            self.onlydirs = list(
                filter(lambda name: name[0] != '.', self.onlydirs))
            self.onlyfiles = list(
                filter(lambda name: name[0] != '.', self.onlyfiles))

        # FILTER FOR HIDDEN FILES
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
        self.currentDirectory += "/" + path
        self.test = path.replace("\n", "")
        self.outwin.refresh()
        self.currentDirectory = self.currentDirectory.replace("\n", "")
        self.inserted_word = ""
        self.create()

    def navigate_back(self):
        self.outwin.erase()
        temp = self.currentDirectory.split("/")
        del temp[-1]
        self.test = str(temp)
        self.outwin.refresh()
        self.currentDirectory = "/".join(temp)
        self.create()

    def run_loop(self):
        while True:
            try:
                if self.inserted_word != "":
                    self.outwin.addstr(self.height-1, 1, str(self.test))
                key = self.outwin.getch()
                self.get_input_key(key)
            except KeyboardInterrupt:
                curses.nocbreak()
                curses.echo()
                curses.curs_set(1)
                curses.endwin()

    def update_selection(self):
        self.run_ls()
        all_files = self.onlydirs + self.onlyfiles
        for x in all_files:
            if x.find(self.inserted_word) == 0:
                self.selected_filename = x
                break

    def get_input_key(self, key):
        """Function that retrieve an input from the user and parse it"""
        self.height, self.width = self.outwin.getmaxyx()
        if key == 10:  # ENTER KEY
            self.navigate_path(self.selected_filename)
            self.create()
        elif key == 127:  # BACKSPACE KEY
            self.navigate_back()
        elif key == 78:  # N maiuscola
            create_new_file(self.currentDirectory)
            self.run_ls()
        elif key == 77:  # M maiuscola
            create_new_folder(self.currentDirectory)
            self.run_ls()
        elif key == 72: # H maiuscola
            self.hide_hidden_files = not self.hide_hidden_files
            self.run_ls()
        elif key == 32:
            show_maintab()
            self.run_ls()
        elif key == 68:
            delete_selected_file(self.selected_filename)
            self.run_ls()
        elif key == curses.KEY_RESIZE:
            self.display_window()
        elif key == 27: # ESC per resettare 
            self.inserted_word = ""
        else:
            self.inserted_word += str(chr(key))
            self.update_selection()


def main():
    WindowFileManager()


if __name__ == "__main__":
    main()
