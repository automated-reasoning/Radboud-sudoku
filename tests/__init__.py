import unittest
from radboud_sudoku.sudoku import Sudoku

class TestSudoku(unittest.TestCase):
    def test_set_and_get(self):
        puzzle = Sudoku()
        self.assertEqual(puzzle.get(2, 3), None)
        puzzle.set(2, 3, 4)
        self.assertEqual(puzzle.get(2, 3), 4)


if __name__ == '__main__':
    unittest.main()
