from collections import namedtuple
import random

NUM_ROWS = 10
NUM_COLS = 17
GOAL = 10
D = 3
Clear = namedtuple('Clear', 'x y width height points')


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
                        yield Clear(sx, sy, width, height, tuple((x, y, grid[y][x])
                                                                 for y in range(sy, sy + height)
                                                                 for x in range(sx, sx + width)
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


def compute_grid_hash(grid):
    grid_hash = 0
    for x in range(NUM_COLS):
        for y in range(NUM_ROWS):
            grid_hash = grid_hash * 11 + grid[y][x]
        grid_hash %= 2 ** 64
    return grid_hash


def solve2(grid, box=None):
    best_cdf = []
    best_clears = []
    best_score = 0
    num_states = 0
    visited_hashes = set()

    def recurse(px, py, score, clears, cdf, min_back_index=1000):
        nonlocal best_cdf, best_clears, best_score

        def process(clear, new_min_back_index):
            nonlocal num_states
            num_states += 1
            if num_states >= 10000:
                return
            clears.append(clear)
            cdf_val = clear.points[0][1] * NUM_COLS + clear.points[0][0]
            for x, y, val in clear.points:
                grid[y][x] = 0
                cdf.append(max(cdf[-1], cdf_val))
            grid_hash = compute_grid_hash(grid)
            if grid_hash not in visited_hashes:
                visited_hashes.add(grid_hash)
                recurse(px, py, score + len(clear.points), clears, cdf, new_min_back_index)
            clears.pop()
            for (x, y, val) in clear.points:
                grid[y][x] = val
                cdf.pop()

        if py == NUM_ROWS:
            if score > best_score:
                best_cdf = cdf.copy()
                best_clears = clears.copy()
                best_score = score
        elif px == NUM_COLS:
            recurse(0, py + 1, score, clears, cdf)
        else:
            if len(best_cdf) > len(cdf) + D and best_cdf[len(cdf) + D] <= cdf[-1]:
                return
            used_clears = set()
            for back_index in range(min_back_index, len(clears)):
                for (cx, cy, _) in clears[back_index].points:
                    for back_clear in find_clears_containing(grid, cx, cy):
                        if back_clear not in used_clears:
                            process(back_clear, back_index)
                            used_clears.add(back_clear)
            for new_clear in find_clears(grid, px, py):
                process(new_clear, len(clears))
            recurse(px + 1, py, score, clears, cdf)

    recurse(0, 0, 0, [], [-1])
    if box:
        for sx, sy, width, height, _ in best_clears:
            box(sx, sy, width, height)
    return best_score


def test():
    grid = [[random.randint(1, 9) for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    for row in grid:
        print(row)
    print('solve1:', solve1(grid))
    print('solve2:', solve2(grid))


# test()
