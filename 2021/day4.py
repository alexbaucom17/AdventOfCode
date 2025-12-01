import sys
sys.path.append('.')
import aoc

data_rows = aoc.get_input(4, sample=False).splitlines()

class Board: 
    def __init__(self, board_rows_str):
        self.board_rows = [[int(val.strip()) for val in (board_rows_str[row].split())] for row in range(len(board_rows_str))]
        self.num_to_idx = {}
        for row in range(len(self.board_rows)):
            for col in range(len(self.board_rows[row])):
                num = self.board_rows[row][col]
                self.num_to_idx[num] = (row, col)

        self.marked = [[False for col in range(len(self.board_rows[row]))] for row in range(len(self.board_rows))]
        self.last_num = -1
        self.won = False

    def score(self):
        running_sum = 0
        for row in range(len(self.board_rows)):
            for col in range(len(self.board_rows[row])):
                if not self.marked[row][col]:
                    running_sum += self.board_rows[row][col]
        return running_sum * self.last_num

    def add(self, num):
        if num not in self.num_to_idx:
            return False
        
        self.last_num = num
        row, col = self.num_to_idx[num]
        self.marked[row][col] = True
        self.won = self._check_win(row, col)
        return self.won

    def _check_win(self, row, col):
        won_row = True
        for r in range(len(self.board_rows)):
            if not self.marked[r][col]:
                won_row = False
                break
        won_col = True
        for c in range(len(self.board_rows[0])):
            if not self.marked[row][c]:
                won_col = False
                break
        return won_col or won_row

    def __str__(self) -> str:
        return f"Nums:\n{self.board_rows}\nMarked:\n{self.marked}\n"

nums = [int(val.strip()) for val in data_rows[0].split(',')]
board_strs = []
for i in range(2, len(data_rows), 6):
    board_strs.append(tuple(data_rows[i+j] for j in range(5)))
boards = [Board(board_str) for board_str in board_strs]

# def part1():
#     for num in nums:
#         for board in boards:
#             if board.add(num):
#                 print(board.score())
#                 return
# part1()

def part2():
    num_won = 0
    next_win = False
    for num in nums:
        for board in boards:
            if board.won:
                continue
            if board.add(num):
                num_won += 1
                if len(boards) == num_won:
                    print(board.score())
                    return
    
part2()