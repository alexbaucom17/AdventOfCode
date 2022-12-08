import sys
sys.path.append('.')
import aoc
import math
from aoc_utils.parsing import int_grid
import numpy as np

data_rows = aoc.get_input(8, sample=False, index=0).splitlines()

def create_visibility_mask(slice):
  max_height = -1
  visibility_mask = [False for i in range(len(slice))]
  for i in range(len(slice)):
    height = slice[i]
    if height > max_height:
      visibility_mask[i] = True
      max_height = height
  return np.asarray(visibility_mask)

def create_scenic_scores(slice):
  scenic_scores = np.zeros_like(slice, dtype=int)
  active_trees = {} # idx:  (height, cur_score)
  for i in range(len(slice)):
    cur_height = slice[i]

    # Update active trees
    clear_idx = []
    for active_idx, data in active_trees.items():
      active_height, active_score = data
      active_score += 1
      if cur_height >= active_height:
        scenic_scores[active_idx] = active_score
        clear_idx.append(active_idx)
      else:
        active_trees[active_idx] = (active_height, active_score)

    # Clear active trees which are not active any more    
    for idx in clear_idx:
      del active_trees[idx]
    
    # Add new tree to active trees
    active_trees[i] = (cur_height, 0)

  # Collect any leftover active trees
  for active_idx, data in active_trees.items():
    scenic_scores[active_idx] = data[1]
  
  return scenic_scores


def part1():
  grid = np.asarray(int_grid(data_rows))
  # print(grid)

  # Left visibility
  left_visibility = np.zeros_like(grid, dtype=bool)
  for row_ix in range(grid.shape[0]):
    row_slice = grid[row_ix, :]
    left_visibility[row_ix, :] = create_visibility_mask(row_slice)
  # print(left_visibility)

  # Right visibility
  right_visibility = np.zeros_like(grid, dtype=bool)
  for row_ix in range(grid.shape[0]):
    row_slice = grid[row_ix, :]
    right_visibility[row_ix, :] = np.flip(create_visibility_mask(np.flip(row_slice)))
  # print(right_visibility)

  # Down visibility
  down_visibility = np.zeros_like(grid, dtype=bool)
  for col_ix in range(grid.shape[1]):
    col_slice = grid[:, col_ix]
    down_visibility[:, col_ix] = create_visibility_mask(col_slice)
  # print(down_visibility)

  # up visibility
  up_visibility = np.zeros_like(grid, dtype=bool)
  for col_ix in range(grid.shape[1]):
    col_slice = grid[:, col_ix]
    up_visibility[:, col_ix] = np.flip(create_visibility_mask(np.flip(col_slice)))
  # print(up_visibility)

  side_visibility = np.logical_or(left_visibility, right_visibility)
  vert_visibility = np.logical_or(up_visibility, down_visibility)
  full_visibility = np.logical_or(side_visibility, vert_visibility)
  # print(full_visibility)
  print(np.sum(np.sum(full_visibility)))  

# part1()

def part2():
  grid = np.asarray(int_grid(data_rows))
  # print(grid)

  right_score = np.zeros_like(grid, dtype=int)
  for row_ix in range(grid.shape[0]):
    row_slice = grid[row_ix, :]
    right_score[row_ix, :] = create_scenic_scores(row_slice)
  # print(right_score)

  left_score = np.zeros_like(grid, dtype=int)
  for row_ix in range(grid.shape[0]):
    row_slice = grid[row_ix, :]
    left_score[row_ix, :] = np.flip(create_scenic_scores(np.flip(row_slice)))
  # print(left_score)

  up_score = np.zeros_like(grid, dtype=int)
  for col_ix in range(grid.shape[1]):
    col_slice = grid[:, col_ix]
    up_score[:, col_ix] = create_scenic_scores(col_slice)
  # print(up_score)

  down_score = np.zeros_like(grid, dtype=int)
  for col_ix in range(grid.shape[1]):
    col_slice = grid[:, col_ix]
    down_score[:, col_ix] = np.flip(create_scenic_scores(np.flip(col_slice)))
  # print(down_score)

  full_score = right_score * left_score * up_score * down_score
  # print(full_score)
  print(np.max(np.max(full_score)))  

part2()