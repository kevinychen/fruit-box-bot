use std::collections::HashSet;
use std::num::Wrapping;

use pyo3::{prelude::*};

const HEIGHT: usize = 10;
const WIDTH: usize = 17;
const MAX_NUM_MOVES: usize = HEIGHT * WIDTH / 2 + 1;
const D: usize = 4;

type Grid = [[u32; WIDTH]; HEIGHT];

#[pyclass]
#[derive(Clone, Copy)]
pub struct Box {
    #[pyo3(get)]
    pub x: usize,
    #[pyo3(get)]
    pub y: usize,
    #[pyo3(get)]
    pub width: usize,
    #[pyo3(get)]
    pub height: usize,
}

#[pyclass]
#[derive(Clone)]
pub struct Strategy {
    #[pyo3(get)]
    pub boxes: Vec<Box>,
    #[pyo3(get)]
    pub score: u32,
}

fn hash(grid: Grid) -> u64 {
    let mut hash = Wrapping(0u64);
    for row in grid.iter() {
        for &value in row.iter() {
            hash = hash * Wrapping(11) + Wrapping(value as u64);
        }
    }
    hash.0
}

fn recurse(
    grid: Grid,
    visited: &mut HashSet<u64>,
    current_strategy: &mut Strategy,
    num_moves: usize,
    best_intermediate_scores: &mut [u32; MAX_NUM_MOVES],
    best_strategy: &mut Strategy,
) {
    if current_strategy.score > best_strategy.score {
        best_strategy.boxes.clear();
        best_strategy.boxes.extend(&current_strategy.boxes);
        best_strategy.score = current_strategy.score;
    }

    if current_strategy.score < best_intermediate_scores[num_moves] {
        best_intermediate_scores[num_moves] = current_strategy.score;
    }
    if current_strategy.score > best_intermediate_scores[num_moves] + 5 {
        return;
    }

    let hash = hash(grid);
    if !visited.insert(hash) {
        return;
    }

    if visited.len() > 100000 {
        return;
    }

    let mut cum_sums = [[0u32; WIDTH + 1]; HEIGHT];
    for i in 0..HEIGHT {
        for j in 1..=WIDTH {
            cum_sums[i][j] = cum_sums[i][j - 1] + grid[i][j - 1];
        }
    }

    let mut moves: [Option<(Box, u32)>; D] = [None; D];
    for x in 0..WIDTH {
        for y in 0..HEIGHT {
            for width in 1..=WIDTH - x {
                let mut sum = 0u32;
                for height in 1..=HEIGHT - y {
                    sum += cum_sums[y + height - 1][x + width] - cum_sums[y + height - 1][x];
                    if sum == 10 {
                        let mut count = 0u32;
                        for xx in x..x + width {
                            for yy in y..y + height {
                                if grid[yy][xx] > 0 {
                                    count += 1;
                                }
                            }
                        }
                        match moves.iter().position(|m| match m {
                            None => true,
                            Some((_, other_count)) => *other_count > count,
                        }) {
                            None => {},
                            Some(index) => {
                                for i in (index + 1..D).rev() {
                                    moves[i] = moves[i - 1];
                                }
                                moves[index] = Some((Box{x, y, width, height}, count));
                            },
                        }
                    }
                }
            }
        }
    }

    for m in moves {
        if let Some((b, count)) = m {
            let Box{x, y, width, height} = b;
            let mut new_grid = grid;
            for xx in x..x + width {
                for yy in y..y + height {
                    new_grid[yy][xx] = 0;
                }
            }
            current_strategy.boxes.push(b);
            current_strategy.score += count;
            recurse(new_grid, visited, current_strategy, num_moves + 1, best_intermediate_scores, best_strategy);
            current_strategy.boxes.pop();
            current_strategy.score -= count;
        }
    }
}

#[pyfunction]
fn find_strategy(grid: Grid) -> PyResult<Strategy> {
    let mut best_strategy = Strategy{boxes: vec![], score: 0};
    recurse(grid, &mut HashSet::new(), &mut Strategy{boxes: vec![], score: 0}, 0, &mut [u32::MAX; MAX_NUM_MOVES], &mut best_strategy);
    Ok(best_strategy)
}

#[pymodule]
fn fruit_box_bot(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Box>()?;
    m.add_class::<Strategy>()?;
    m.add_function(wrap_pyfunction!(find_strategy, m)?)?;
    Ok(())
}
