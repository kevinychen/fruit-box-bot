from collections import namedtuple
from random import randint

NUM_ROWS = 6
NUM_COLS = 6
GOAL = 10
Clear = namedtuple('Clear', 'width height points')


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
                rect_sum += sum([grid[sy + height][x] for x in range(sx, sx + width)])
                leftmost_col_used |= grid[sy + height][sx]
                rightmost_col_used |= grid[sy + height][sx + width - 1]
                height += 1
                if rect_sum > GOAL:
                    break
                if rect_sum == GOAL:
                    if leftmost_col_used and rightmost_col_used:
                        yield Clear(width, height, tuple((x, y, grid[y][x])
                                                    for x in range(sx, sx + width)
                                                    for y in range(sy, sy + height)
                                                    if grid[y][x]))
                    break
        sx -= 1


def find_clears_containing(grid, cx, cy):
    py = cy
    col_sum = 0
    while py >= 0:
        col_sum += grid[py][cx]
        if col_sum >= GOAL:
            break
        px = cx
        rect_sum = 0
        while px >= 0:
            rect_sum += sum([grid[y][px] for y in range(py, cy + 1)])
            if rect_sum > GOAL:
                break
            if grid[py][px]:
                for clear in find_clears(grid, px, py):
                    if clear.width > cx - px and clear.height > cy - py:
                        yield clear
            px -= 1
        px = cx
        rect_sum = 0
        while px < NUM_COLS:
            rect_sum += sum([grid[y][px] for y in range(py, cy + 1)])
            if rect_sum > GOAL:
                break
            if grid[py][px]:
                for clear in find_clears(grid, px, py):
                    if clear.width > px - cx and clear.height > cy - py:
                        yield clear
                break
            px += 1
        py -= 1


def solve2(grid, box=None):
    best_score = 0

    def recurse(px, py, score, clears, min_back_index=1000):
        nonlocal best_score

        def process(clear, new_min_back_index):
            clears.append(clear)
            for (x, y, val) in clear.points:
                grid[y][x] = 0
            recurse(px, py, score + len(clear.points), clears, new_min_back_index)
            clears.pop()
            for (x, y, val) in clear.points:
                grid[y][x] = val

        if py == NUM_ROWS:
            # print(score, clears)
            if score > best_score:
                best_score = score
        elif px == NUM_COLS:
            recurse(0, py + 1, score, clears)
        else:
            used_clears = set()
            for back_index in range(min_back_index, len(clears)):
                for (cx, cy, _) in clears[back_index].points:
                    for back_clear in find_clears_containing(grid, cx, cy):
                        if back_clear not in used_clears:
                            process(back_clear, back_index)
                            used_clears.add(back_clear)
            for new_clear in find_clears(grid, px, py):
                process(new_clear, len(clears))
            recurse(px + 1, py, score, clears)

    recurse(0, 0, 0, [])
    return best_score


def test():
    grid = [[randint(1, 9) for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    for row in grid:
        print(row)
    print('solve1:', solve1(grid))
    print('solve2:', solve2(grid))


test()
