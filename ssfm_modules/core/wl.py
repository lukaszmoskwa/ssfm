# coding=utf-8

import curses
import os
import sys
import subprocess
from os.path import isfile, join, isdir, islink
from math import ceil, floor
from ssfm_modules.draw.draw_mod import draw_file, draw_folder
from ssfm_modules.draw.space_tab import showMainTabDialog


class WindowList:
    outwin = ""
    currentDirectory = ""
    local_id = ""
    onlydirs = []
    onlyfiles = []
    onlylinks = []
    selected_filename = ".."  
    selected_index = []
    height = 0
    width = 0
    inserted_word = ""
    test = ""
    hide_hidden_files = True
    n_pages = 1
    curr_page = 1

    file_dimension = {
        "x": 8,
        "y": 5
    }
    pos_idx = {
        "x": 1,
        "y": 4
    }

    def __init__(self, window_file_manager, vsplit=1, local_id=0):
        if len(sys.argv) > 1 and sys.argv[1] == ".":
            self.currentDirectory = os.getcwd()
        else:
            os.chdir(os.path.expandvars("$HOME"))
            self.currentDirectory = os.getcwd()

        self.theme = window_file_manager.theme
        self.wfm = window_file_manager
        self.local_id = local_id
        self.vsplit = vsplit
        self.height, self.width = window_file_manager.totalwin.getmaxyx()
        self.width = floor(self.width / vsplit)
        self.outwin = window_file_manager.totalwin.subwin(
            self.height, self.width, 0, local_id * self.width)
        self.outwin.box()
        try:
            self.run_ls()
            self.run_draw()
        except:
            self.currentDirectory = "/"
            self.create()

    def create(self):
        self.run_ls()
        self.run_draw()

    def add_file_to_screen(self, filename, isDir, isSelected):
        """Function to add a folder or a file to the screen"""
        background = curses.color_pair(2)
        pos = self.pos_idx
        dim = self.file_dimension
        if self.pos_idx["x"] + dim["x"] > self.width-1:
            pos["x"] = 1
            pos["y"] += dim["y"] + 1
        if pos["y"] + dim["y"] + 1 < self.height:
            if isDir:
                draw_folder(self, isSelected, self.theme)
            else:
                draw_file(self, isSelected, self.theme)

            # TODO Move to draw
            self.outwin.addstr(pos["y"]+dim["y"] - 1, pos["x"] + floor((dim["x"] - len(filename[:dim["x"]]))/2), filename[:dim["x"]],
                               background | curses.A_NORMAL | curses.A_BOLD | curses.A_UNDERLINE
                               if isDir else
                               background)
        self.pos_idx["x"] += dim["x"] + 1

    def run_ls(self):
        """Function used to run the ls command in the current directory and call the add_file_to_screen"""
        self.onlyfiles = [f for f in os.listdir(
            self.currentDirectory) if isfile(join(self.currentDirectory, f))]
        self.onlydirs = [f for f in os.listdir(
            self.currentDirectory) if isdir(join(self.currentDirectory, f))]
        self.onlylinks = [f for f in os.listdir(
            self.currentDirectory) if islink(join(self.currentDirectory, f))]
        # Alphabetic sort
        self.onlydirs.sort()
        self.onlyfiles.sort()

    def run_draw(self):
        self.pos_idx = {
            "x": 1,
            "y": 2
        }
        # Necessary for resize
        self.outwin.clear()
        self.outwin.refresh()
        self.height, self.width = self.wfm.totalwin.getmaxyx()
        self.width = self.width // self.wfm.division
        self.outwin = self.wfm.totalwin.subpad(
            self.height, self.width, 0, self.local_id * self.width)
        self.outwin.box()
        self.outwin.bkgd(' ', curses.color_pair(
            2) | curses.A_BOLD | curses.A_REVERSE)

        # Filter for hidden files
        if self.hide_hidden_files:
            self.onlydirs = list(
                filter(lambda name: name[0] != '.', self.onlydirs))
            self.onlyfiles = list(
                filter(lambda name: name[0] != '.', self.onlyfiles))

        self.onlydirs = [a for a in self.onlydirs if a not in self.onlylinks]
        self.onlyfiles = [a for a in self.onlyfiles if a not in self.onlylinks]

        # Add paging information
        self.outwin.addstr(0, 0, ' '*self.width, curses.A_REVERSE |
                           curses.color_pair(1))
        self.outwin.addstr(0, 0, self.currentDirectory,
                           curses.A_REVERSE | curses.color_pair(1))
        all_files = self.onlydirs + self.onlyfiles
        n_all_files = len(self.onlydirs) - \
            len(self.onlylinks) + len(self.onlyfiles)

        file_per_row = floor((self.width - 1) / (self.file_dimension["x"] + 1))
        self.displayed_files = file_per_row * floor(
            (self.height) / (self.file_dimension["y"] + 2))

        self.n_pages = ceil(n_all_files / self.displayed_files)
        page_string = "[Page " + \
            str(self.curr_page) + "/" + str(self.n_pages) + "]"
        self.outwin.addstr(0, self.width - len(page_string) - 2,
                           page_string, curses.A_REVERSE | curses.color_pair(1))

        # Draw files / folders
        for el in all_files[(self.curr_page - 1) * self.displayed_files:]:
            self.add_file_to_screen(
                el, isdir(el), el != self.selected_filename)
        self.outwin.refresh()

    def display_window(self):
        """Function used to update the window and refresh the screen on resize"""
        self.outwin.clear()
        self.outwin.refresh()
        self.create()

    def navigate_path(self, path):
        """Function to change the currentDirectory path and create the window again"""
        self.outwin.erase()
        try:
            os.chdir(self.currentDirectory)
            os.chdir(path)
        except:
            self.wfm.close("Permission Error")
        self.currentDirectory = os.getcwd()
        self.reset_input()
        self.run_ls()
        self.run_draw()

    def navigate_back(self):
        self.outwin.erase()
        os.chdir(self.currentDirectory)
        os.chdir("..")
        self.currentDirectory = os.getcwd()
        self.reset_input()
        self.run_ls()
        self.run_draw()

    def reset_input(self):
        self.inserted_word = ""
        self.selected_filename = ".."

    def update_selection(self):
        all_files = self.onlydirs + self.onlyfiles
        for (i, x) in enumerate(all_files):
            if x.lower().find(self.inserted_word.lower()) == 0:
                self.selected_filename = x
                self.curr_page = floor(i / self.displayed_files) + 1
                self.selected_index = [i]
                self.test = self.selected_filename
                break
        self.run_draw()

    def arrow_handler(self, key):
        if key == curses.KEY_LEFT:
            self.arrow_navigate("LEFT", False)
        elif key == curses.KEY_RIGHT:
            self.arrow_navigate("RIGHT", False)
        elif key == curses.KEY_UP:
            self.arrow_navigate("UP", False)
        elif key == curses.KEY_DOWN:
            self.arrow_navigate("DOWN", False)

    def next_page(self):
        self.curr_page = min(
            self.n_pages, (self.curr_page + 1) % (self.n_pages + 2))

    def prev_page(self):
        self.curr_page = max(1, (self.curr_page - 1) % (self.n_pages + 1))

    def arrow_navigate(self, direction, hasShift):
        all_files = self.onlydirs + self.onlyfiles
        if not all_files:
            return
        file_per_row = floor((self.width - 1) / (self.file_dimension["x"] + 1))
        current_index = 0
        if self.selected_filename != "..":
            current_index = all_files.index(self.selected_filename)
            if direction == "RIGHT":
                self.selected_filename = all_files[min(
                    len(all_files) - 1, current_index + 1)]
            elif direction == "LEFT":
                self.selected_filename = all_files[max(0, current_index - 1)]
            elif direction == "UP":
                self.selected_filename = all_files[max(
                    0, current_index - file_per_row)]
            elif direction == "DOWN":
                self.selected_filename = all_files[min(
                    len(all_files) - 1, current_index + file_per_row)]
        else:
            self.selected_filename = all_files[current_index]
        current_index = all_files.index(self.selected_filename)
        self.curr_page = (floor(current_index / self.displayed_files)) + 1
        self.run_draw()

    def get_input_key(self, key):
        """Function that retrieve an input from the user and parse it"""
        self.height, self.width = self.outwin.getmaxyx()
        if key == curses.KEY_ENTER or key == 10:  # ENTER KEY
            if not isfile(self.selected_filename):
                self.navigate_path(self.selected_filename)
                self.create()
            else:
                subprocess.call(["xdg-open", self.selected_filename])
                self.inserted_word = ""
                curses.curs_set(0)
                self.wfm.totalwin.keypad(1)
        elif key == curses.KEY_BACKSPACE:  # BACKSPACE KEY
            self.navigate_back()
        elif key == curses.KEY_NPAGE:
            self.next_page()
        elif key == curses.KEY_PPAGE:
            self.prev_page()
        elif key == 72:  # H maiuscola
            self.hide_hidden_files = not self.hide_hidden_files
            self.run_ls()
        elif key == 32:
            showMainTabDialog(theme=self.theme, wfm=self.wfm)
        elif key in (curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN):
            self.arrow_handler(key)
        elif key == 27:  # ESC for reset
            self.inserted_word = ""
        else:
            self.inserted_word += str(chr(key))
            self.update_selection()
