import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;

public class FruitBoxSolver {

    static final String INPUT = "input.dat";
    static final String OUTPUT = "output.dat";

    static final int NUM_COLS = 17;
    static final int NUM_ROWS = 10;
    static final int GOAL = 10;
    static final int D = 5;
    static final int LIMIT = 10000000;

    List<Integer> best_cdf = new ArrayList<>();
    List<Clear> best_clears = new ArrayList<>();
    int best_score;
    int num_states;
    Set<Long> visited_hashes = new HashSet<>();

    public static void main(String[] args) throws IOException {
        new FruitBoxSolver().run();
    }

    void run() throws IOException {
        int[][] grid = new int[NUM_ROWS][];
        List<String> lines = Files.readAllLines(Paths.get(INPUT));
        for (int i = 0; i < NUM_ROWS; i++)
            grid[i] = Arrays.stream(lines.get(i).split(" "))
                .mapToInt(Integer::parseInt)
                .toArray();
        recurse(grid, 0, 0, 0, new ArrayList<>(),
            new ArrayList<>(Arrays.asList(-1)), 1000);
        Files.write(Paths.get(OUTPUT), best_clears.stream()
            .map(clear -> String.format("%s %s %s %s", clear.sx, clear.sy, clear.width, clear.height))
            .collect(Collectors.toList()));
    }

    void recurse(int[][] grid, int px, int py, int score, List<Clear> clears, List<Integer> cdf,
        int min_back_index) {
        if (py == NUM_ROWS) {
            if (score > best_score) {
                best_cdf = new ArrayList<>(cdf);
                best_clears = new ArrayList<>(clears);
                best_score = score;
            }
        } else if (px == NUM_COLS)
            recurse(grid, 0, py + 1, score, clears, cdf, 1000);
        else {
            if (best_cdf.size() > cdf.size() + D && best_cdf.get(cdf.size() + D) <= last(cdf))
                return;
            Set<Clear> used_clears = new HashSet<>();
            for (int back_index = min_back_index; back_index < clears.size(); back_index++)
                for (Point p : clears.get(back_index).points)
                    for (Clear back_clear : find_clears_containing(grid, p.x, p.y))
                        if (!used_clears.contains(back_clear)) {
                            process(grid, px, py, score, clears, cdf, back_clear, back_index);
                            used_clears.add(back_clear);
                        }
            for (Clear new_clear : find_clears(grid, px, py))
                process(grid, px, py, score, clears, cdf, new_clear, clears.size());
            recurse(grid, px + 1, py, score, clears, cdf, 1000);
        }
    }

    void process(int[][] grid, int px, int py, int score, List<Clear> clears, List<Integer> cdf,
        Clear clear, int new_min_back_index) {
        num_states += 1;
        if (num_states >= LIMIT)
            return;
        clears.add(clear);
        int cdf_val = clear.points.get(0).y * NUM_COLS + clear.points.get(0).x;
        for (Point p : clear.points) {
            grid[p.y][p.x] = 0;
            cdf.add(Math.max(last(cdf), cdf_val));
        }
        long grid_hash = compute_grid_hash(grid);
        if (!visited_hashes.contains(grid_hash)) {
            visited_hashes.add(grid_hash);
            recurse(grid, px, py, score + clear.points.size(), clears, cdf, new_min_back_index);
        }
        removeLast(clears);
        for (Point p : clear.points) {
            grid[p.y][p.x] = p.val;
            removeLast(cdf);
        }
    }

    List<Clear> find_clears_containing(int[][] grid, int cx, int cy) {
        List<Clear> clears = new ArrayList<>();
        int py = cy;
        int col_sum = 0;
        while (py >= 0) {
            col_sum += grid[py][cx];
            if (col_sum >= GOAL)
                break;
            int px = cx;
            int rect_sum = 0;
            while (px >= 0) {
                for (int y = py; y < cy + 1; y++)
                    rect_sum += grid[y][px];
                if (rect_sum > GOAL)
                    break;
                if (grid[py][px] > 0)
                    for (Clear clear : find_clears(grid, px, py))
                        if (clear.width > cx - px && clear.height > cy - py)
                            clears.add(clear);
                px -= 1;
            }
            px = cx;
            rect_sum = 0;
            while (px < NUM_COLS) {
                for (int y = py; y < cy + 1; y++)
                    rect_sum += grid[y][px];
                if (rect_sum > GOAL)
                    break;
                if (grid[py][px] > 0) {
                    for (Clear clear : find_clears(grid, px, py))
                        if (clear.width > px - cx && clear.height > cy - py)
                            clears.add(clear);
                    break;
                }
                px += 1;
            }
            py -= 1;
        }
        return clears;
    }

    List<Clear> find_clears(int[][] grid, int px, int py) {
        List<Clear> clears = new ArrayList<>();
        if (grid[py][px] == 0)
            return clears;
        int sx = px, sy = py;
        while (sx >= 0 && (sx == px || grid[sy][sx] == 0)) {
            int width = px - sx;
            int row_sum = 0;
            while (sx + width < NUM_COLS) {
                row_sum += grid[sy][sx + width];
                width += 1;
                if (row_sum > GOAL)
                    break;
                int height = 0;
                int rect_sum = 0;
                boolean leftmost_col_used = false;
                boolean rightmost_col_used = false;
                while(sy + height < NUM_ROWS) {
                    for (int x = sx; x < sx + width; x++)
                        rect_sum += grid[sy + height][x];
                    leftmost_col_used |= grid[sy + height][sx] > 0;
                    rightmost_col_used |= grid[sy + height][sx + width - 1] > 0;
                    height += 1;
                    if (rect_sum > GOAL)
                        break;
                    if (rect_sum == GOAL) {
                        if (leftmost_col_used && rightmost_col_used) {
                            List<Point> points = new ArrayList<>();
                            for (int x = sx; x < sx + width; x++)
                                for (int y = sy; y < sy + height; y++)
                                    if (grid[y][x] > 0)
                                        points.add(new Point(x, y, grid[y][x]));
                            clears.add(new Clear(sx, sy, width, height, points));
                        }
                        break;
                    }
                }
            }
            sx -= 1;
        }
        return clears;
    }

    long compute_grid_hash(int[][] grid) {
        long grid_hash = 0;
        for (int x = 0; x < NUM_COLS; x++)
            for (int y = 0; y < NUM_ROWS; y++)
                grid_hash = grid_hash * 11 + grid[y][x];
        return grid_hash;
    }

    <T> T last(List<T> list) {
        return list.get(list.size() - 1);
    }

    <T> T removeLast(List<T> list) {
        return list.remove(list.size() - 1);
    }

    static class Clear {
        final int sx, sy, width, height;
        final List<Point> points;

        public Clear(int sx, int sy, int width, int height, List<Point> points) {
            this.sx = sx;
            this.sy = sy;
            this.width = width;
            this.height = height;
            this.points = points;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o)
                return true;
            if (o == null || getClass() != o.getClass())
                return false;
            Clear clear = (Clear) o;
            return sx == clear.sx && sy == clear.sy && width == clear.width
                && height == clear.height && Objects.equals(points, clear.points);
        }

        @Override
        public int hashCode() {
            return Objects.hash(sx, sy, width, height, points);
        }
    }

    static class Point {
        final int x, y, val;

        Point(int x, int y, int val) {
            this.x = x;
            this.y = y;
            this.val = val;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o)
                return true;
            if (o == null || getClass() != o.getClass())
                return false;
            Point point = (Point) o;
            return x == point.x && y == point.y && val == point.val;
        }

        @Override
        public int hashCode() {
            return Objects.hash(x, y, val);
        }
    }
}

