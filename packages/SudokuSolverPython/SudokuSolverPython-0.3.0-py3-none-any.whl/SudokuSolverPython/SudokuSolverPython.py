class Sudoku:
    def __init__(self, board):
        self.board = board

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else '.' for num in row))

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, num, pos):
        row, col = pos
        if num in self.board[row]:
            return False
        if num in [self.board[i][col] for i in range(9)]:
            return False
        box_row, box_col = row // 3 * 3, col // 3 * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def is_board_valid(self):
        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                if num != 0:
                    self.board[i][j] = 0
                    if not self.is_valid(num, (i, j)):
                        return False
                    self.board[i][j] = num
        return True

    def has_enough_facts(self):
        empty_cells = sum(row.count(0) for row in self.board)
        filled_cells = 81 - empty_cells
        return filled_cells >= 17

    def solve(self):
        if not self.has_enough_facts():
            print("Недостаточное количество фактов для решения")
            return False
        if not self.is_board_valid():
            print("Несовместный набор фактов")
            return False
        empty = self.find_empty()
        if not empty:
            print("Точное решение:")
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False

start_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
