
import curses
from modules.extensions.window_extension.window_handler import WindowExtension
from modules.extensions.file_extension.file_handler import FileExtension
from modules.extensions.git_extension.git_handler import GitExtension


class SpaceTab():
    pass


class BaseTabDialog:
    def __init__(self, **options):
        self.wfm = options.get('wfm')
        self.maxy, self.maxx = self.wfm.height, self.wfm.width
        self.theme = options.get('theme')
        self.win = curses.newwin(12, self.maxx - 2, self.maxy - 13, 1)
        self.win.bkgd(' ', curses.color_pair(
            2) | curses.A_BOLD | curses.A_REVERSE)
        self.win.box()
        self.y, self.x = self.win.getmaxyx()
        self.win.keypad(1)
        self.enterKey = False
        self.win.keypad(1)
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()


class MainTabDialog(BaseTabDialog):
    def showMainTab(self):
        # TODO Move in configs 
        curses.curs_set(0)
        options = {
            'f': ('file', FileExtension),
            'w': ('window', WindowExtension),
            #'b': ('bookmark', WindowExtension),
            'g': ('git', GitExtension),
            #'s': ('settings', WindowExtension),
        }
        for (i, x) in enumerate(options.keys()):
            self.win.addstr(i+1, 2, "[" + x + "] " +
                            options[x][0], curses.color_pair(2) | curses.A_NORMAL)
        key = self.win.getch()
        if key in map(lambda x: ord(x), options.keys()):
            self.win.clear()
            self.win.box()
            self.display_options(options[chr(key)][1]().get_options())
            options[chr(key)][1]().handle(self.win.getch(), self.wfm)

    def display_options(self, options):
        for (i, x) in enumerate(options):
            self.win.addstr(i+1, 2, "[" + x[0] + "] " +
                            x[1], curses.color_pair(2) | curses.A_NORMAL)


def showMainTabDialog(**options):
    return MainTabDialog(**options).showMainTab()


def displayTabOptions(**options):
    return MainTabDialog(**options).display_options(options=options)
