"""
Contains the SmtBasedSolver class.
"""
import typing

# TODO sadly, no typing support for z3 based types right now.
import z3 as smtapi  # type: ignore

from radboudsudoku.sudoku import Sudoku, SudokuRectangularBlock


class SmtBasedSolver:
    """
    This SMT-based Sudoku solver uses the z3py API.
    """

    def __init__(self):
        self._smt_solver = smtapi.Solver()
        self._cell_variables = {}

    def encode(self, puzzle: Sudoku):
        """
        Takes a puzzle and encodes it into the SMT solver.
        :param puzzle:
        :return:
        """
        # We first create the variables and store them for future access in the object.
        self._create_variables(puzzle)
        # We then encode the puzzle
        self._add_constraints(puzzle)

    def _create_variables(self, puzzle: Sudoku) -> None:
        """
        Creates an integer variable for every cell
        :param puzzle: The sudoku.
        """
        for cell in puzzle.cells:
            self._cell_variables[cell] = smtapi.Int(f"v-{cell.row}-{cell.column}")

    def _add_constraints(self, puzzle: Sudoku) -> None:
        """

        :param puzzle:
        :return:
        """
        # 1. Each cell should be filled with an allowed value.
        for cell in puzzle.cells:
            current_value = puzzle.get_value(cell.row, cell.column)
            if current_value is None:
                self._add_either_value(self._cell_variables[cell], puzzle.allowed_values)
            else:
                self._smt_solver.add(self._cell_variables[cell] == current_value)
        # 2. The values for the cells in every row should be distinct.
        for row in puzzle.row_indices:
            self._add_all_different(self._row_variables(puzzle, row))
        # 3. The values for the cells in every column should be distinct.
        for column in puzzle.column_indices:
            self._add_all_different(self._column_variables(puzzle, column))
        # 4. The values for the cells in every block should be distinct.
        for block in puzzle.blocks:
            self._add_all_different(self._block_variables(block))
        # Note that in standard sudokus, 1+2 encodes that every value must be used in every row.
        # Likewise, 1+3 and 1+4 ensure this for columns and blocks, respectively.
        # Debugging tip: Here you can export all constraints via print(self._smt_solver)

    def _row_variables(self, puzzle: Sudoku, row: int) -> list[smtapi.Int]:
        return [self._cell_variables[cell] for cell in puzzle.cells_for_row(row)]

    def _column_variables(self, puzzle: Sudoku, column: int) -> list[smtapi.Int]:
        return [self._cell_variables[cell] for cell in puzzle.cells_for_column(column)]

    def _block_variables(self, block: SudokuRectangularBlock):
        return [self._cell_variables[cell] for cell in block.cells]

    def _add_all_different(self, variables) -> None:
        for index, lhs_var in enumerate(variables):
            for rhs_var in variables[index + 1 :]:
                self._smt_solver.add(lhs_var != rhs_var)

    def _add_either_value(self, variable: smtapi.Int, values: typing.Iterable[int]) -> None:
        self._smt_solver.add(smtapi.Or([variable == v for v in values]))

    def solve(self, puzzle) -> tuple[bool, typing.Any]:
        """
        Solves a puzzle after encoding
        :param puzzle:
        :return:
        """
        solved = self._smt_solver.check()
        if solved == smtapi.sat:
            model = self._smt_solver.model()
            result = {}
            for cell in puzzle.cells:
                result[cell] = model.evaluate(self._cell_variables[cell])
            return True, result
        return False, None
