__version__ = '0.1.0'

from math import hypot
from pyautogui import drag, easeOutQuad, leftClick, locateAll, locateOnScreen, moveTo, screenshot

NUM_ROWS = 10
NUM_COLS = 17
SIZE = 66
EDGE = 15
SCALE = 2  # Screenshotting a retina display gives 2x the dimensions

left, top, _, _ = locateOnScreen('reset.png', confidence=0.99)
left += 16
top -= 726
leftClick(x=left / SCALE, y=top / SCALE)

while True:
    image = screenshot()
    grid = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    for digit in range(1, 10):
        for (local_left, local_top, _, _) in locateAll(f'apple{digit}.png', image, confidence=0.99):
            x, y = (local_left - left - EDGE) // SIZE, (local_top - top - EDGE) // SIZE
            grid[y][x] = digit
    dims = [(width, height) for width in range(1, NUM_COLS) for height in range(1, NUM_ROWS)]
    found = False
    for (width, height) in sorted(dims, key=max):
        for x in range(NUM_COLS - width + 1):
            for y in range(NUM_ROWS - height + 1):
                if sum([grid[y + dy][x + dx] for dx in range(width) for dy in range(height)]) == 10:
                    moveTo((left + x * SIZE) / SCALE, (top + y * SIZE) / SCALE)
                    duration = 0.1 * hypot(width, height)
                    drag(width * SIZE / SCALE, height * SIZE / SCALE, duration, easeOutQuad, button='left')
                    found = True
                    for dx in range(width):
                        for dy in range(height):
                            grid[y + dy][x + dx] = 0
    if not found:
        break
