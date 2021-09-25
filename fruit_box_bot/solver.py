from collections import namedtuple
from random import randint

NUM_ROWS = 4
NUM_COLS = 4
GOAL = 10
Clear = namedtuple('Clear', 'x y width height num')


def solve1(grid, box=None):
    grid = [[grid[y][x] for x in range(NUM_COLS)] for y in range(NUM_ROWS)]
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


def find_clears(grid, px, py):
    if grid[py][px] == 0:
        return
    sx, sy = px, py
    while sx >= 0 and (sx == px or grid[sy][sx] == 0):
        width = px - sx
        row_sum = 0
        while sx + width < NUM_COLS:
            row_sum += grid[sy][sx + width]
            width += 1
            if row_sum > GOAL:
                break
            height = 0
            rect_sum = 0
            leftmost_col_used = False
            rightmost_col_used = False
            while sy + height < NUM_ROWS:
                rect_sum += row_sum if height == 0 else sum([grid[sy + height][x] for x in range(sx, sx + width)])
                leftmost_col_used |= grid[sy + height][sx]
                rightmost_col_used |= grid[sy + height][sx + width - 1]
                height += 1
                if rect_sum > GOAL:
                    break
                if rect_sum == GOAL:
                    if leftmost_col_used and rightmost_col_used:
                        yield [(x, y, grid[y][x])
                               for x in range(sx, sx + width) for y in range(sy, sy + height) if grid[y][x]]
                    break
        sx -= 1


def solve2(grid, box=None):
    best_clears = []

    def recurse(px, py, score, clears):
        if py == NUM_ROWS:
            print("#", score, clears)
        elif px == NUM_COLS:
            recurse(0, py + 1, score, clears)
        else:
            if clears:
                for (x, y, val) in clears[-1]:
                    # TODO
                    pass
            recurse(px + 1, py, score, clears)
            for clear in find_clears(grid, px, py):
                clears.append(clear)
                for (x, y, val) in clear:
                    grid[y][x] = 0
                recurse(px + 1, py, score + len(clear), clears)
                clears.pop()
                for (x, y, val) in clear:
                    grid[y][x] = val

    recurse(0, 0, 0, [])


grid = [
    [1, 0, 0, 9, 0],
    [9, 8, 0, 2, 0],
    [0, 0, 5, 3, 0],
    [1, 2, 3, 1, 0],
]
solve2(grid)


import math
def test(n: int):
    print('testing', n, 'cases...')
    scores1 = [solve1([[randint(1, 9) for x in range(NUM_COLS)] for y in range(NUM_ROWS)]) for _ in range(n)]
    # scores2 = [solve2([[randint(1, 9) for x in range(NUM_COLS)] for y in range(NUM_ROWS)]) for _ in range(n)]
    mean = sum(scores1) / len(scores1)
    print('score: ', sum(scores1) / len(scores1))
    print('stddev: ', math.sqrt(sum([(score - mean) ** 2 for score in scores1]) / n))
    # print('score: ', sum(scores2) / len(scores2))


# test(400)
