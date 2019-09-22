import curses


class BaseDialog:
    def __init__(self, **options):
        self.maxy, self.maxx = curses.LINES, curses.COLS
        self.win = curses.newwin(12, 56, int(
            (self.maxy/2)-6), int((self.maxx/2)-28))
        self.win.box()
        self.y, self.x = self.win.getmaxyx()
        self.title_attr = options.get(
            'title_attr', curses.A_BOLD | curses.A_STANDOUT)
        self.msg_attr = options.get('msg_attr',   curses.A_BOLD)
        self.opt_attr = options.get('opt_attr',   curses.A_BOLD)
        self.focus_attr = options.get(
            'focus_attr', curses.A_BOLD | curses.A_STANDOUT)
        self.title = options.get('title',      curses.A_NORMAL)
        self.message = options.get('message', '')
        self.win.addstr(0, 0, ' '*56, self.title_attr)
        self.win.keypad(1)
        self.focus = 0
        self.enterKey = False
        self.win.keypad(1)
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()


def rectangle(win, begin_y, begin_x, height, width, attr):
    win.vline(begin_y,    begin_x,       curses.ACS_VLINE, height, attr)
    win.hline(begin_y,        begin_x,   curses.ACS_HLINE, width, attr)
    win.hline(height+begin_y, begin_x,   curses.ACS_HLINE, width, attr)
    win.vline(begin_y,    begin_x+width, curses.ACS_VLINE, height, attr)
    win.addch(begin_y,        begin_x,       curses.ACS_ULCORNER,  attr)
    win.addch(begin_y,        begin_x+width, curses.ACS_URCORNER,  attr)
    win.addch(height+begin_y, begin_x,       curses.ACS_LLCORNER,  attr)
    win.addch(begin_y+height, begin_x+width, curses.ACS_LRCORNER,  attr)
    win.refresh()



