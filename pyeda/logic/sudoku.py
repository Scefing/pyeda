"""
Logic functions for Sudoku
"""

# Disable "invalid variable name"
# pylint: disable=C0103

from pyeda.boolalg.expr import And, OneHot
from pyeda.boolalg.vexpr import bitvec

DIGITS = "123456789"


class SudokuSolver(object):
    """Logical constraints for 3x3 Sudoku"""

    def __init__(self, varname='x'):
        self.X = bitvec(varname, (1, 10), (1, 10), (1, 10))
        self.V = And(*[
                     And(*[OneHot(*[self.X[r][c][v] for v in range(1, 10)])
                           for c in range(1, 10)])
                       for r in range(1, 10)])
        self.R = And(*[
                     And(*[OneHot(*[self.X[r][c][v] for c in range(1, 10)])
                           for v in range(1, 10)])
                       for r in range(1, 10)])
        self.C = And(*[
                     And(*[OneHot(*[self.X[r][c][v] for r in range(1, 10)])
                           for v in range(1, 10)])
                       for c in range(1, 10)])
        self.B = And(*[
                     And(*[OneHot(*[self.X[3*br+r][3*bc+c][v]
                                    for r in range(1, 4)
                                    for c in range(1, 4)])
                           for v in range(1, 10)])
                       for br in range(3) for bc in range(3)])
        self.S = And(self.V, self.R, self.C, self.B)

    def solve(self, grid):
        """Return a solution point for a Sudoku grid."""
        I = self._parse_grid(grid)
        return (self.S * I).satisfy_one()

    def display_solve(self, grid):
        """Return a solution point for a Sudoku grid as a string."""
        return self._soln2str(self.solve(grid))

    def _parse_grid(self, grid):
        """Return the input constraints for a Sudoku grid."""
        chars = [c for c in grid if c in DIGITS or c in "0."]
        if len(chars) != 9 ** 2:
            raise ValueError("expected 9x9 grid")
        I = And(*[ self.X[i // 9 + 1][i % 9 + 1][int(c)]
                   for i, c in enumerate(chars) if c in DIGITS ])
        return I

    def _soln2str(self, soln, fancy=False):
        """Convert a Sudoku solution point to a string."""
        chars = list()
        for r in range(1, 10):
            for c in range(1, 10):
                if fancy and c in (4, 7):
                    chars.append("|")
                chars.append(self._get_val(soln, r, c))
            if fancy and r != 9:
                chars.append("\n")
                if r in (3, 6):
                    chars.append("---+---+---\n")
        return "".join(chars)

    def _get_val(self, soln, r, c):
        """Return the string value for a solution coordinate."""
        for v in range(1, 10):
            if soln[self.X[r][c][v]]:
                return DIGITS[v-1]
        return "X"
