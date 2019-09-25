import curses
from ssfm_modules.core.wl import WindowList

class WindowFileManager:
    theme = {
        'foreground': 32,
        'background': 232
    }
    totalwin = ""
    outwin_list = []
    height = ""
    window_focus = 0
    division = 1
    width = ""
    copy_path = ""
    is_copy = True # False if cut

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
                curses.init_pair(i, i, -1)
            curses.init_pair(1, self.theme['foreground'], self.theme['background'])
            curses.init_pair(2, self.theme['background'], self.theme['foreground'])
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

    def close(self, err_string=""):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()
        if err_string != "":
            print(err_string)
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
                