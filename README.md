# RadboudSudoku

-----

## Installation

The solver is not yet on pypi. You can install from the source.

The easiest way to run the command line is via
```
hatch run radboudsudoku resources/sudokus/volkskrant_24_08_2023.csv
```

This requires `hatch` on your system. `hatch` will ensure that you have all dependencies,
and that the installation of this project does not collide with any other version of the dependencies that you may have on your system.
More information on `hatch` and its installation can be found at their [website](https://hatch.pypa.io/latest/).

## Code structure

* The main source code is in `src/radboudsudoku`, in particular,
  - `sudoku.py` provides data structures for the puzzle, and parsing capabilities
  - `smtbasedsolver.py` presents an smt-based solver.
  - the `cli/__init__py` presents a small command line interface.

## License

`radboudsudoku` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
