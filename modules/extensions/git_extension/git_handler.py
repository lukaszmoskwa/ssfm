import curses
import subprocess
from modules.extensions.extension_handler import ExtensionHandler


class GitExtension(ExtensionHandler):

    options = [
        ('g', 'summary'),
        ('s', 'git status'),
        ('l', 'git log'),
    ]

    def handle(self, character, wfm):
        if character == ord('g'):
            self.git_summary()
        elif character == ord('l'):
            self.git_log()
        elif character == ord('s'):
            self.git_status()


    def git_summary(self):
        subprocess.run(["tig"], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

    def git_status(self):
        """ Run the command to open tig status"""
        subprocess.run(["tig", "status"], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

    def git_log(self):
        subprocess.run(["tig", "log"], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
