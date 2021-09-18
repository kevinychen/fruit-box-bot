__version__ = '0.1.0'

from math import hypot
from pyautogui import drag, easeOutQuad, leftClick, locateAll, locateOnScreen, moveTo, screenshot
import solver

NUM_ROWS = 10
NUM_COLS = 17
SIZE = 66
EDGE = 15
SCALE = 2  # Screenshotting a retina display gives 2x the dimensions

left, top, _, _ = locateOnScreen('reset.png', confidence=0.99)
left += 16
top -= 726
leftClick(x=left / SCALE, y=top / SCALE)


def box(x, y, width, height):
    moveTo((left + x * SIZE) / SCALE, (top + y * SIZE) / SCALE)
    duration = 0.1 * hypot(width, height)
    drag(width * SIZE / SCALE, height * SIZE / SCALE, duration, easeOutQuad, button='left')


while True:
    leftClick(x=(left - 6) / SCALE, y=(top + 736) / SCALE)
    leftClick(x=(left + 300) / SCALE, y=(top + 350) / SCALE)
    image = screenshot()
    grid = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    for digit in range(1, 10):
        for (local_left, local_top, _, _) in locateAll(f'apple{digit}.png', image, confidence=0.99):
            grid[(local_top - top - EDGE) // SIZE][(local_left - left - EDGE) // SIZE] = digit
    score = solver.solve1(grid)
    print(score)
    if score >= 140:
        break
solver.solve1(grid, box)
