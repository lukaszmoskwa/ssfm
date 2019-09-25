
import ssfm_modules.core.wl
from ssfm_modules.extensions.extension_handler import ExtensionHandler


class WindowExtension(ExtensionHandler):
    
    options = [
        ('w', 'switch focus'),
        ('n', 'new window'),
        ('d', 'delete current window'),
    ]

    def handle(self, character, wfm):
        if character == ord('w'):
            self.switch_focus(wfm)
        elif character == ord('d'):
            self.close_window(wfm)
        elif character == ord('n'):
            self.new_window(wfm)

    def switch_focus(self, wfm):
        wfm.window_focus += 1
        wfm.window_focus %= wfm.division

    def new_window(self, wfm):
        wfm.division += 1
        wfm.outwin_list.append(ssfm_modules.core.wl.WindowList(
            wfm, wfm.division, wfm.division - 1))
        self.switch_focus(wfm)
        wfm.redraw()

    def close_window(self, wfm):
        del wfm.outwin_list[wfm.window_focus]
        wfm.division -= 1
        if wfm.division == 0:
            wfm.close()
        for (i, x) in enumerate(wfm.outwin_list):
            x.local_id = i
        self.switch_focus(wfm)
        wfm.redraw()
