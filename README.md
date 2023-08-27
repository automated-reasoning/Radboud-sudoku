# RadboudSudoku

-----

## Installation

The solver is not yet on pypi. You can install from the source.

The easiest way to run the command line is via
```
hatch run radboudsudoku resources/sudokus/volkskrant_24_08_2023.csv
```

## Code structure

* The main source code is in `src/radboud_sudoku`, in particular,
  - `sudoku.py` provides data structures for the puzzle, and parsing capabilities
  - `smtbasedsolver.py` presents an Smt solver.
  - the `cli/__init__py` presents a small command line interface.
* Some test cases are presented in `tests/` and also highlight the usage of the API.

## License

`radboudsudoku` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
