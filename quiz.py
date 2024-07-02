from random import randint
from test_data import *
from pprint import pprint

# quiz.py

def reverse_list(l:list):
    length = 0
    for item in l:
        length += 1
    ls_done = []
    i = 0
    j = -1
    while (length + j) not in ls_done:
        temp = l[j]
        l[j] = l[i]
        l[i] = temp
        ls_done += [i]
        i += 1
        j -= 1

    return l


def solve_sudoku(matrix):
    def is_valid(r, c, v, matrix):
        if v in matrix[r]:
            return False

        column = [matrix[i][c] for i in range(9)]
        if v in column:
            return False

        x = r // 3
        y = c // 3
        for i in range(3):
            for j in range(3):
                if matrix[3 * x + i][3 * y + j] == v:
                    return False

        return True

    def solve_board(matrix):
        for i in range(9):
            for j in range(9):
                if matrix[i][j] == 0:
                    for v in range(1, 10):
                        if is_valid(i, j, v, matrix):
                            matrix[i][j] = v
                            if solve_board(matrix):
                                return True
                            matrix[i][j] = 0
                    return False
        return True

    if solve_board(matrix):
        return matrix
    else:
        return "No solution"


if __name__ == '__main__':
    # result = reverse_list([1,4,7,9,13,100])
    result = solve_sudoku(sudoku1)
    pprint(result)
