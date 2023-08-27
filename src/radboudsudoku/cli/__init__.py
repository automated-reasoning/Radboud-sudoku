"""
A command line interface to our solver.
"""

import copy

import click

import radboudsudoku.smtbasedsolver as smtsolver
from radboudsudoku.__about__ import __version__
from radboudsudoku.sudoku import parse_from_csv, write_to_csv


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="RadboudSudoku")
@click.argument("puzzle")
def radboudsudoku(puzzle):
    """
    This is a command line interface that solves Sudokus, given in an CSV file, using an SMT-solver.

    TODO: The export to the solution.csv is undocumented and not configurable.
    TODO: The paths are not checked for existence.
    :return:
    """
    puzzle = parse_from_csv(puzzle)
    solver = smtsolver.SmtBasedSolver()
    solver.encode(puzzle)
    solved, solution = solver.solve(puzzle)
    if solved:
        print("Solution found!")

        # create a copy that will be filled
        solution_puzzle = copy.deepcopy(puzzle)
        # Write the solution into the puzzle
        for cell, value in solution.items():
            solution_puzzle.set_value(cell.row, cell.column, value)
        write_to_csv("solution.csv", solution_puzzle)
        # Check whether the solution is a valid solution
        try:
            solution_puzzle.check_is_valid()
        except Exception as exc:
            msg = "The solver yielded an invalid solution!"
            raise RuntimeError(msg) from exc
        # Check that we properly deepcopied this earlier, just for demonstration purposes
        assert not puzzle.is_filled()

    else:
        print("No solution!")
