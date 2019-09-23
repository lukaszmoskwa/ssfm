import curses


class BaseDialog:
    def __init__(self, **options):
        self.maxy, self.maxx = curses.LINES, curses.COLS
        self.win = curses.newwin(12, 42, int(
            (self.maxy/2)-5), int((self.maxx/2)-24))
        self.win.box()
        self.win.bkgd(' ', curses.color_pair(1))
        self.y, self.x = self.win.getmaxyx()
        self.title_attr = options.get(
            'title_attr', curses.A_BOLD | curses.A_STANDOUT)
        self.msg_attr = options.get('msg_attr',   curses.A_BOLD)
        self.opt_attr = options.get('opt_attr',   curses.A_BOLD)
        self.focus_attr = options.get(
            'focus_attr', curses.A_BOLD | curses.A_STANDOUT)
        self.title = options.get(
            'title', curses.A_REVERSE | curses.color_pair(1))
        self.message = options.get('message', '')
        self.win.addstr(0, 0, ' '*42, curses.color_pair(2))
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


class AskYesCancelDialog(BaseDialog):


    def left_right_key_event_handler(self, max):
        self.win.refresh()
        key = self.win.getch()
        if key == curses.KEY_LEFT and self.focus != 0:
            self.focus -= 1
        elif key == curses.KEY_RIGHT and self.focus != max-1:
            self.focus += 1
        elif key == ord('\n'):
            self.enterKey = True


    def askYesOrCancel(self):
        if self.title:
            self.win.addstr(0, int(self.x/2 - len(self.title)/2),
                            self.title, self.title_attr)
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i+1, 2, msg,  self.msg_attr)
        option = ('Yes   ', 'No    ')
        rectangle(self.win, 8, 5, 2, len(option[0])+1, self.opt_attr)
        rectangle(self.win, 8, 23, 2, len(option[1])+1, self.opt_attr)
        pos_x = [6, 24]
        while self.enterKey != True:
            if self.enterKey == 27:
                break

            if self.focus == 0:
                self.win.addstr(9, pos_x[0], ' Yes  ',
                                self.focus_attr | self.opt_attr)
            else:
                self.win.addstr(9, pos_x[0], ' Yes  ',    self.opt_attr)

            if self.focus == 1:
                self.win.addstr(9, pos_x[1], ' No   ',
                                self.focus_attr | self.opt_attr)
            else:
                self.win.addstr(9, pos_x[1], ' No   ', self.opt_attr)
            for i in range(2):
                if i != self.focus:
                    rectangle(
                        self.win, 8, pos_x[i]-1, 2, len(option[i])+1, curses.A_NORMAL | self.opt_attr)
                else:
                    rectangle(self.win, 8, pos_x[self.focus]-1, 2, len(
                        option[self.focus])+1, self.focus_attr | self.opt_attr)
            self.left_right_key_event_handler(2)
        if self.focus == 0:
            return True
        return False
