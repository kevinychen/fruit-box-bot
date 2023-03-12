__version__ = '0.1.0'

from math import hypot
from pyautogui import drag, easeOutQuad, leftClick, locateAllOnScreen, locateOnScreen, moveTo
import fruit_box_bot

NUM_ROWS = 10
NUM_COLS = 17
SCALE = 2  # Screenshotting a retina display gives 2x the dimensions
SIZE = 33 * SCALE

# Find reset button to get game bounds
left, top, _, _ = locateOnScreen('images/reset.png', confidence=0.99)
left += 8 * SCALE
top -= 363 * SCALE
region = (left, top, SIZE * NUM_COLS, SIZE * NUM_ROWS)
leftClick(x=left / SCALE, y=top / SCALE)

while True:
    leftClick(x=left / SCALE - 3, y=top / SCALE + 368)  # Click "Reset"
    leftClick(x=left / SCALE + 150, y=top / SCALE + 175)  # Click "Play"

    # Figure out the apple values
    grid = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    total = 0
    for digit in range(1, 10):
        for (local_left, local_top, _, _) in locateAllOnScreen(f'images/apple{digit}.png', region=region, confidence=0.99):
            grid[(local_top - top) // SIZE][(local_left - left) // SIZE] = digit
            total += digit

    # Optimization: grids with lower sums generally give higher scores
    if total > 800:
        continue

    strategy = fruit_box_bot.find_strategy(grid)
    print(f'Sum of apples: {total}; Found strategy with score {strategy.score}')

    # If we're aiming for a particular score, exit early if we didn't get it
    if strategy.score < NUM_ROWS * NUM_COLS:
        continue

    # Play the game
    for box in strategy.boxes:
        moveTo((left + box.x * SIZE) / SCALE, (top + box.y * SIZE) / SCALE)
        duration = 0.08 * hypot(box.width, box.height)
        drag(box.width * SIZE / SCALE, box.height * SIZE / SCALE, duration, easeOutQuad, button='left')
    break
