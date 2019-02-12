import collections
import shelve

import pkg_resources
import pyscreeze
from pyscreeze import Box
import pyautogui as gui


class Asset:
    def __init__(self, tl, br):
        self.tl = tl
        self.br = br
        self.bounds = Box(0, 0, 0, 0)
        self.b_tl = self.b_br = Box(0, 0, 0, 0)

        self.calibrate()

    def calibrate(self):
        self.b_tl = gui.locateOnScreen(self.tl)
        self.b_br = gui.locateOnScreen(self.br)

        self.bounds = Box(
            self.b_tl.left, self.b_tl.top,
            self.b_br.left + self.b_br.width - self.b_tl.left,
            self.b_br.top + self.b_br.height - self.b_tl.top
        )

    def verify(self):
        try:
            # these will raise ImageNotFoundException if failed
            gui.locate(self.tl, gui.screenshot(region=self.b_tl))
            gui.locate(self.br, gui.screenshot(region=self.b_br))
            return True
        except pyscreeze.ImageNotFoundException:
            return False


class Grid(Asset):
    def __init__(self, tl, br, size):
        super(Grid, self).__init__(tl, br)
        self.size = size

    def __getitem__(self, coord):
        x, y = coord
        xx = int(self.bounds.left + (x + .5) * self.bounds.width / self.size)
        yy = int(self.bounds.top + (y + .5) * self.bounds.height / self.size)
        return xx, yy


Grids = collections.namedtuple('Grids', ('me', 'other'))


def load(cache_file=None):
    with shelve.open(cache_file) as shelf:
        try:
            if 'grid_me' not in shelf or not shelf['grid_me'].verify():
                print('relocating own grid')

                shelf['grid_me'] = Grid(pkg_resources.resource_filename('autobattleship', 'res/pri_tl.png'),
                                        pkg_resources.resource_filename('autobattleship', 'res/pri_br.png'),
                                        size=10)

            if 'grid_other' not in shelf or not shelf['grid_other'].verify():
                print('relocating target grid')
                
                shelf['grid_other'] = Grid(pkg_resources.resource_filename('autobattleship', 'res/sec_tl.png'),
                                           pkg_resources.resource_filename('autobattleship', 'res/sec_br.png'),
                                           size=10)

            return Grids(shelf['grid_me'], shelf['grid_other'])
        except pyscreeze.ImageNotFoundException:
            print('could not locate grids')
            quit(-1)
