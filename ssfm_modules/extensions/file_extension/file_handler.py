import curses
import subprocess
import os
import time
import shutil
from os.path import isdir, isfile
import ssfm_modules.draw.space_tab
from ssfm_modules.extensions.extension_handler import ExtensionHandler
from ssfm_modules.draw.dialogs import BaseDialog, rectangle, AskYesCancelDialog


class CreateFile(BaseDialog):
    def file_save(self):
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
        self.win.addstr(3, 2, 'Type here:')
        self.win.addstr(4, 2, ' '*0, curses.A_UNDERLINE)
        filepath = ''
        while True:
            car = self.win.getch()
            if car == 27:
                filepath = None
                break
            elif car == 127:
                filepath = filepath[:-1]
                self.win.addstr(4, 2, filepath, curses.A_UNDERLINE)
                continue
            elif car == 10:
                if filepath == '': 
                    filepath = None
                break
            else:
                car = chr(car)
                filepath += car

        return filepath


def createFileDialog(**options):
    return CreateFile(**options).file_save()


class FileExtension(ExtensionHandler):

    options = [
        ['n', 'new file'],
        ['m', 'new folder'],
        ['e', 'edit file'],
        ['r', 'rename'],
        ['d', 'delete file or folder'],
        ['y', 'copy'],
        ['x', 'cut'],
        ['p', 'paste [ ]'],
    ]

    def handle(self, character, wfm):
        self.wfm = wfm
        self.outwin = wfm.outwin_list[wfm.window_focus]
        if character == ord('n'):
            self.create_new_file(self.outwin.currentDirectory)
        elif character == ord('e'):
            self.edit_file_or_folder(self.outwin.selected_filename)
        elif character == ord('d'):
            self.delete_file_or_folder(self.outwin.selected_filename)
        elif character == ord('m'):
            self.create_new_folder(self.outwin.currentDirectory)
        elif character == ord('y'):
            self.copy_file(self.outwin.currentDirectory)
        elif character == ord('p'):
            self.paste_file(self.outwin.currentDirectory)
        elif character == ord('r'):
            self.rename_file()

        if self.wfm.copy_path != "":
            self.options[-1][1] = "paste [ " + self.wfm.copy_path + " ]"
        else:
            self.options[-1][1] = "paste [ ]"

        self.outwin.run_ls()
        self.outwin.run_draw()
        self.outwin.selected_filename = '..'
        curses.curs_set(0)

    def create_new_file(self, cwd):
        """ Run the command to create a new file"""
        filepath = createFileDialog(
            message='Choose a name for the new file',
            title='Create new file')
        if filepath != None:
            subprocess.run(["touch", filepath],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def edit_file_or_folder(self, path):
        if path == '..':
            path = '.'
        if isdir(path):
            subprocess.run(["vim", path],  # TODO substitute with custom editor
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.run(["vim", path])  # TODO substitute with custom editor
            self.wfm.totalwin.keypad(1)

    def delete_file_or_folder(self, path):
        if path == '..':
            return
        message = 'Are you sure you want to delete\n'
        message += 'Folder: ' if isdir(path) else 'File: '
        message += path
        confirm = AskYesCancelDialog(
            message=message, title='Delete ' + path).askYesOrCancel()
        if confirm:
            if isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    def create_new_folder(self, cwd):
        """ Run the command to create a new folder """
        filepath = createFileDialog(
            message='Choose a name for the new folder',
            title='Create new folder')
        if filepath != None:
            try:
                os.mkdir(filepath)
            except FileExistsError:
                pass

    def rename_file(self):
        """ Run the command to rename a file or folder """
        src = self.outwin.selected_filename
        name = createFileDialog(
            message='Rename ' + ( 'folder' if isdir(self.outwin.selected_filename) else 'file' ) ,
            title='Rename')
        if name != None:
            try:
                os.rename(src, name)
            except FileExistsError:
                pass

    def copy_file(self, cwd):
        filename = self.outwin.selected_filename
        if filename == "..":
            return
        self.wfm.is_copy = True
        self.wfm.copy_path = cwd + "/" + filename
        self.outwin.reset_input()
        self.show_rectangle("   Copied   ")

    def cut_file(self, cwd):
        filename = self.outwin.selected_filename
        if filename == "..":
            return
        self.wfm.is_copy = False
        self.wfm.copy_path = cwd + "/" + filename
        self.outwin.reset_input()
        self.show_rectangle("   Cut    ")


    def show_rectangle(self, temp):
        rectangle(self.outwin.outwin, self.outwin.height //
                  2 - 2, (self.outwin.width // 2) - 7, 4, 14, 0)
        self.outwin.outwin.addstr(self.outwin.height // 2 - 1,
                                  (self.outwin.width // 2) - len(temp)//2, " " * (len(temp) + 1), curses.A_REVERSE | curses.A_BOLD)
        self.outwin.outwin.addstr(self.outwin.height // 2,
                                  (self.outwin.width // 2) - len(temp)//2, temp, curses.A_REVERSE | curses.A_BOLD)
        self.outwin.outwin.addstr(self.outwin.height // 2 + 1,
                                  (self.outwin.width // 2) - len(temp)//2, " " * (len(temp) + 1), curses.A_REVERSE | curses.A_BOLD)
        self.outwin.outwin.refresh()
        time.sleep(0.5)

    def paste_file(self, cwd):
        src = self.wfm.copy_path
        dst = cwd + "/" + os.path.basename(src)
        try:
            if self.wfm.is_copy:
                if isdir(src):
                    shutil.copytree(src, dst)
                elif isfile(src):
                    shutil.copy2(src,dst)
            else:
                shutil.move(src, dst)

            self.wfm.copy_path = ""
            self.outwin.reset_input()
        except:
            self.show_rectangle("  Error   ")
            pass
