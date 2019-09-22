import curses
from modules.core.wl import WindowList

class WindowFileManager:
    theme_number = 13
    totalwin = ""
    outwin_list = []
    height = ""
    window_focus = 0
    division = 1
    width = ""

    def __init__(self):
        self.create()
        self.run_loop()

    def create(self):
        """Function used to create the screen"""

        self.totalwin = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.totalwin.keypad(1)
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            for i in range(0, curses.COLORS):
                curses.init_pair(i + 1, i, -1)
        self.height, self.width = self.totalwin.getmaxyx()
        self.totalwin.box()
        self.outwin_list.append(WindowList(self, self.division, 0))

    def redraw(self):
        self.totalwin.clear()
        self.height, self.width = self.totalwin.getmaxyx()
        for i in self.outwin_list:
            i.outwin.clear()
            i.outwin.refresh()
        for i in self.outwin_list:
            i.run_draw()

    def close(self):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()
        quit()


    def run_loop(self):
        while True:
            try:
                key = self.totalwin.getch()
                if key == curses.KEY_RESIZE:
                    self.redraw()
                    continue

                self.outwin_list[self.window_focus].get_input_key(key)
                self.outwin_list[self.window_focus].run_draw()
            except KeyboardInterrupt:
                self.close()
                