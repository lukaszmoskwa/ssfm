# coding=utf-8

import curses
import os
from os.path import isfile, join
import sys
import locale 
from math import ceil

locale.setlocale(locale.LC_ALL, '')
reload(sys)
sys.setdefaultencoding('utf8')



class WindowFileManager:
    outwin =""
    currentDirectory = ""
    onlydirs = []
    onlyfiles = []
    file_dimension = {
        "x": 8,
        "y": 5
    }
    pos_idx = {
        "x" : 1,
        "y" : 1
    }
    selected_filename = ".." # FIX THIS
    height = 0
    width = 0 
    UP = -1
    DOWN = 1
    TOP = 0
    BOTTOM = 0
    CURRENT_CURSOR = 0
    inserted_word = ""
    test = ""

    def __init__(self):
        self.currentDirectory = "/home/lukasz"
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
        self.height, self.width = self.outwin.getmaxyx()
        self.outwin.box()
        self.run_ls()
    
    def add_file_to_screen(self, filename, isDir):
        """Function to add a folder or a file to the screen"""
        pos = self.pos_idx
        dim = self.file_dimension
        self.pos_idx["x"] += dim["x"] + 1
        if self.pos_idx["x"] + dim["x"] > self.width-1:
            pos["x"] = 1
            pos["y"] += dim["y"] + 1
        if pos["y"] + dim["y"] + 1 < self.height:
            self.draw_folder() if isDir else self.draw_file()
            # Add file name
            self.outwin.addstr(pos["y"]+dim["y"] -1, pos["x"], filename[:dim["x"]], curses.A_UNDERLINE if isDir else curses.A_NORMAL )

    def run_ls(self):
        """Function used to run the ls command in the current directory and call the add_file_to_screen"""
        self.onlyfiles = [f for f in os.listdir(self.currentDirectory) if isfile(join(self.currentDirectory, f))]
        self.onlydirs = [f for f in os.listdir(self.currentDirectory) if not isfile(join(self.currentDirectory, f))]
        self.pos_idx = {
            "x" : 1,
            "y" : 1
        }
        self.files_on_screen = len(self.onlydirs) + len(self.onlyfiles)
        self.BOTTOM = ceil(self.files_on_screen / (self.width // self.file_dimension["x"] + 1)) * (self.file_dimension["y"] + 1)
        for el in self.onlydirs:
            self.add_file_to_screen(el, True)
        for el in self.onlyfiles:
            self.add_file_to_screen(el, False)

    def draw_folder(self):
        """Function used to draw the folder"""
        pos = self.pos_idx
        dim = self.file_dimension
        up_dir = "┏━━┓"
        up_dir = up_dir.encode("utf-8", "ignore").decode("utf-8")
        self.outwin.addstr(pos["y"], pos["x"]+dim["x"]-4, up_dir)
        for y in range(1, dim["y"]-1):
            for x in range(0, dim["x"]):
                if y == 1:
                    self.outwin.addstr(pos["y"] + y, pos["x"] + x, "┏" if x==0  else ("┃" if x==dim["x"]-1 else ("┛" if x==dim["x"]-4 else "━")), curses.A_NORMAL)
                elif y == dim["y"]-2:
                    self.outwin.addstr(pos["y"] + y, pos["x"] + x, "┗" if x==0  else ("┛" if x==dim["x"]-1 else "━"), curses.A_NORMAL)
                else:
                    self.outwin.addstr(pos["y"] + y, pos["x"] + x, "┃" if x==0 or x==dim["x"]-1 else " ")
    
    def draw_file(self):
        """Function used to draw the file"""
        pos = self.pos_idx
        dim = self.file_dimension
        for y in range(0, dim["y"]-1):
            for x in range(0, dim["x"]):
                if y == 0:
                    self.outwin.addstr(pos["y"] + y, pos["x"] + x, "┏" if x==0  else ("┓" if x==dim["x"]-1 else "━"), curses.A_NORMAL)
                elif y == dim["y"]-2:
                    self.outwin.addstr(pos["y"] + y, pos["x"] + x, "┗" if x==0  else ("┛" if x==dim["x"]-1 else "━"), curses.A_NORMAL)
                else:
                    self.outwin.addstr(pos["y"] + y, pos["x"] + x, "┃" if x==0 or x==dim["x"]-1 else "-")

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

    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""
        # next cursor position after scrolling
        next_line = self.CURRENT_CURSOR + direction

        # Up direction scroll overflow
        # current cursor position is 0, but top position is greater than 0
        if (direction == self.UP) and (self.TOP > 0 and self.CURRENT_CURSOR == 0):
            self.TOP += direction
            return
        # Down direction scroll overflow
        # next cursor position touch the max lines, but absolute position of max lines could not touch the bottom
        if (direction == self.DOWN) and (next_line == self.height) and (self.TOP + self.height < self.BOTTOM):
            self.top += direction
            return
        # Scroll up
        # current cursor position or top position is greater than 0
        if (direction == self.UP) and (self.TOP > 0 or self.CURRENT_CURSOR > 0):
            self.current = next_line
            return
        # Scroll down
        # next cursor position is above max lines, and absolute position of next cursor could not touch the bottom
        if (direction == self.DOWN) and (next_line < self.height) and (self.TOP + next_line < self.BOTTOM):
            self.current = next_line
            return

    def get_input_key(self, key):
        """Function that retrieve an input from the user and parse it"""
        self.height, self.width = self.outwin.getmaxyx()
        if key==10: # ENTER KEY
            self.navigate_path(self.inserted_word)
            self.create()
        elif key==127: # BACKSPACE KEY
            self.navigate_back()
        elif key==curses.KEY_RESIZE:
            self.display_window()
        elif key==27:
            self.inserted_word = ""
        else:
            self.inserted_word += str(chr(key))

def main():
    WindowFileManager()

if __name__ == "__main__":
    main()
