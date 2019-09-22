
import modules.core.wl
from modules.extensions.extension_handler import ExtensionHandler

class WindowExtension(ExtensionHandler):

    def handle(self, character, wfm):
        window_handle(character, wfm)

def window_handle(key, wfm):
    if key == ord('w'):
        switch_focus(wfm)
    elif key == ord('d'):
        close_window(wfm)
    elif key == ord('n'):
        new_window(wfm)


def switch_focus(wfm):
    wfm.window_focus += 1
    wfm.window_focus %= wfm.division

def new_window(wfm):
    wfm.division += 1
    wfm.outwin_list.append(modules.core.wl.WindowList(wfm, wfm.division, wfm.division -1))
    switch_focus(wfm)
    wfm.redraw()


def close_window(wfm):
    del wfm.outwin_list[wfm.window_focus]
    wfm.division -= 1
    for (i, x) in enumerate(wfm.outwin_list):
        x.local_id = i
    switch_focus(wfm)
    wfm.redraw()
