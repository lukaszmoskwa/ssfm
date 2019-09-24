from modules.curs_dialog import *
import subprocess


def delete_selected_file(filename):
    """Run the command to delete a file/folder"""
    result = askYesCancelDialog(
        message='Are you sure you want to delete ' + str(filename),
        title='Delete selected',
        title_attr=curses.A_STANDOUT | curses.A_BOLD
    )


