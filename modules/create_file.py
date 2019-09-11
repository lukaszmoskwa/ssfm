from modules.curs_dialog import *
import subprocess


def delete_selected_file(filename):
    """Run the command to delete a file/folder"""
    result = askYesCancelDialog(
        message='Are you sure you want to delete ' + str(filename),
        title='Delete selected',
        title_attr=curses.A_STANDOUT | curses.A_BOLD
    )

def show_maintab():
    """Show the maintab """
    cose = showMainTabDialog()


def create_new_file(cwd):
    """ Run the command to create a new file"""
    filepath = createFileDialog(
        message='Choose a name for the new file',
        title='Create new file')
    if filepath != None:
        subprocess.run(["touch", str(cwd) + "/" + filepath],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def create_new_folder(cwd):
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
