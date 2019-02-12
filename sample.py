import pyautogui as gui
import autobattleship as ship

from autobattleship import assets

g = assets.load('loc.cache')

for x in range(10):
    gui.moveTo(*g.me[x, 0], pause=.125)
for y in range(10):
    gui.moveTo(*g.me[0, y], pause=.125)

for x in range(10):
    gui.moveTo(*g.other[x, 0], pause=.125)
for y in range(10):
    gui.moveTo(*g.other[0, y], pause=.125)

gui.moveTo(*g.other[5, 7])
