from collections import namedtuple
from random import randint

NUM_ROWS = 10
NUM_COLS = 17
GOAL = 10
Clear = namedtuple('Clear', 'x y width height num')


def solve1(grid, box=None):
    dims = [(width, height) for width in range(1, NUM_COLS) for height in range(1, NUM_ROWS)]
    while True:
        found = False
        for (width, height) in sorted(dims, key=max):
            for x in range(NUM_COLS - width + 1):
                for y in range(NUM_ROWS - height + 1):
                    if sum([grid[y + dy][x + dx] for dx in range(width) for dy in range(height)]) == GOAL:
                        found = True
                        for dx in range(width):
                            for dy in range(height):
                                grid[y + dy][x + dx] = 0
                        if box:
                            box(x, y, width, height)
        if not found:
            break
    return sum([grid[y][x] == 0 for x in range(NUM_COLS) for y in range(NUM_ROWS)])


def num_rectangles(grid):
    num = 0
    sums = [[0 for _ in range(NUM_COLS + 1)] for _ in range(NUM_ROWS)]
    for x in range(NUM_COLS):
        for y in range(NUM_ROWS):
            sums[y][x + 1] = sums[y][x] + grid[y][x]
    for x in range(NUM_COLS):
        for y in range(NUM_ROWS):
            for width in range(1, NUM_COLS - x + 1):
                total = 0
                for height in range(1, NUM_ROWS - y + 1):
                    total += sums[y + height - 1][x + width] - sums[y + height - 1][x]
                    if total > GOAL:
                        break
                    if total == GOAL:
                        num += 1
    return num


def solve2(grid, box=None):
    while True:
        all_clears = []
        sums = [[0 for _ in range(NUM_COLS + 1)] for _ in range(NUM_ROWS)]
        for x in range(NUM_COLS):
            for y in range(NUM_ROWS):
                sums[y][x + 1] = sums[y][x] + grid[y][x]
        for x in range(NUM_COLS):
            for y in range(NUM_ROWS):
                for width in range(1, NUM_COLS - x + 1):
                    total = 0
                    for height in range(1, NUM_ROWS - y + 1):
                        total += sums[y + height - 1][x + width] - sums[y + height - 1][x]
                        if total > GOAL:
                            break
                        if total == GOAL:
                            clears = []
                            for dx in range(width):
                                for dy in range(height):
                                    val = grid[y + dy][x + dx]
                                    if val > 0:
                                        clears.append((x + dx, y + dy, val))
                                        grid[y + dy][x + dx] = 0
                            all_clears.append(Clear(x, y, width, height, num_rectangles(grid)))
                            for (clear_x, clear_y, val) in clears:
                                grid[clear_y][clear_x] = val
        if not all_clears:
            break
        x, y, width, height, _ = max(all_clears, key=lambda clear: clear.num - 10 * (clear.width + clear.height))
        for dx in range(width):
            for dy in range(height):
                grid[y + dy][x + dx] = 0
        if box:
            box(x, y, width, height)
    return sum([grid[y][x] == 0 for x in range(NUM_COLS) for y in range(NUM_ROWS)])


import math
def test(n: int):
    print('testing', n, 'cases...')
    scores1 = [solve1([[randint(1, 9) for x in range(NUM_COLS)] for y in range(NUM_ROWS)]) for _ in range(n)]
    # scores2 = [solve2([[randint(1, 9) for x in range(NUM_COLS)] for y in range(NUM_ROWS)]) for _ in range(n)]
    mean = sum(scores1) / len(scores1)
    print('score: ', sum(scores1) / len(scores1))
    print('stddev: ', math.sqrt(sum([(score - mean) ** 2 for score in scores1]) / n))
    # print('score: ', sum(scores2) / len(scores2))


test(400)
