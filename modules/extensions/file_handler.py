
import subprocess
from modules.extensions.extension_handler import ExtensionHandler
from modules.curs_dialog import createFileDialog, showMessageDialog

class FileExtension(ExtensionHandler):

    def handle(self, character, wfm):
        pass

    def create_file(self):
        pass

    def create_new_file(self, cwd):
        """ Run the command to create a new file"""
        filepath = createFileDialog(
            message='Choose a name for the new file',
            title='Create new file')
        if filepath != None:
            subprocess.run(["touch", str(cwd) + "/" + filepath],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
      

