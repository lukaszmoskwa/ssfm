import curses
import subprocess
from os.path import isdir, isfile
import modules.draw.space_tab
from modules.extensions.extension_handler import ExtensionHandler
from modules.draw.dialogs import BaseDialog, rectangle


class CreateFile(BaseDialog):
    def fileSave(self):
        if self.title:
            self.win.addstr(0, int(self.x/2-len(self.title)/2),
                            self.title, self.title_attr)
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i+1, 2, msg, self.msg_attr)

        option = 'Save as'
        space = int(self.x/6)
        pos_x = []

        pos_x.append(space)
        rectangle(self.win, 8, space-1, 2, len(option)+1, self.opt_attr)
        space = space + len(option) + 8

        self.win.addstr(9, pos_x[0], 'Create ',
                        self.focus_attr | self.opt_attr)

        rectangle(self.win, 8, pos_x[self.focus]-1, 2,
                  len(option)+1, self.focus_attr | self.opt_attr)
        filepath = None

        curses.echo()
        curses.cbreak()
        curses.curs_set(1)
        self.win.keypad(False)
        self.win.addstr(4, 2, 'Type here:')
        self.win.addstr(6, 2, ' '*0, curses.A_UNDERLINE)
        filepath = ''
        while True:
            car = self.win.getch()
            if car == 27:
                filepath = None
                break
            elif car == 127:
                self.win.delch()
            elif car == 10:
                if filepath == '':  # TODO Serve davvero?
                    filepath = None
                break
            else:
                car = chr(car)
                filepath += car
            #filepath = self.win.getstr(6, 2, curses.A_BOLD).decode('latin1')

        return filepath


def createFileDialog(**options):
    return CreateFile(**options).fileSave()


class FileExtension(ExtensionHandler):

    options = [
        ('n', 'new file'),
        ('e', 'edit file'),
    ]

    def handle(self, character, wfm):
        self.wfm = wfm
        if character == ord('n'):
            self.create_new_file(
                wfm.outwin_list[wfm.window_focus].currentDirectory)
        elif character == ord('e'):
            outwin = wfm.outwin_list[wfm.window_focus]
            self.edit_file_or_folder(outwin.selected_filename)


    def create_new_file(self, cwd):
        """ Run the command to create a new file"""
        filepath = createFileDialog(
            message='Choose a name for the new file',
            title='Create new file')
        if filepath != None:
            subprocess.run(["touch", str(cwd) + "/" + filepath],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def edit_file_or_folder(self, path):
        if path == '..':
            path = '.'
        if isdir(path):
            subprocess.run(["code", path],  # TODO substitute with custom editor
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.run(["vim", path])  # TODO substitute with custom editor
            self.wfm.totalwin.keypad(1)

    def create_new_folder(self, cwd):
        """ Run the command to create a new folder """
        filepath = createFileDialog(
            message='Choose a name for the new folder',
            title='Create new folder')
        if filepath != None:
            proc = subprocess.run(["mkdir", str(cwd) + "/" + filepath],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            text = str(proc.stderr).encode("utf-8").decode("utf-8")
        if text != "b''":
            showMessageDialog(message=text, title='Display message ')
