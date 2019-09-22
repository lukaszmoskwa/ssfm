
import curses
from modules.extensions.window_handler import window_handle


class SpaceTab():
    pass


class BaseTabDialog:
    def __init__(self, **options):
        self.wfm = options.get('wfm')
        self.maxy, self.maxx = self.wfm.height, self.wfm.width
        self.theme = options.get('theme')
        self.win = curses.newwin(12, self.maxx - 2, self.maxy - 12, 1)
        self.win.bkgd(' ', curses.color_pair(self.theme) | curses.A_BOLD)
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
        # TODO Spostare nelle configurazioni per rendere piu estensibile

        # Creare un file 'git.py' in cui passo solo una lettera e in base a quello chiamo una funzione
        options = [
            ('file', 'f'),
            ('window', 'w'),
            ('bookmark', 'b'),
            ('git', 'g'),
            ('settings', 's'),
        ]
        for (i, x) in enumerate(options):
            self.win.addstr(i+1, 2, "[" + x[1] + "] " +
                            x[0], curses.color_pair(self.theme))
        key = self.win.getch()
        if key in map(lambda x: ord(x[1]), options):
            self.win.clear()
            self.win.box()
            if key == ord('w'):
                window_handle(self.win.getch(), self.wfm)


def showMainTabDialog(**options):
    return MainTabDialog(**options).showMainTab()
