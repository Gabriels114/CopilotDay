import random
from dataclasses import dataclass
from typing import Tuple

from mole import Mole, MoleState


@dataclass(frozen=True)
class Board:
    rows: int
    cols: int
    moles: Tuple[Mole, ...]

    @classmethod
    def create(cls, rows: int, cols: int) -> "Board":
        moles = tuple(Mole() for _ in range(rows * cols))
        return cls(rows=rows, cols=cols, moles=moles)

    def _in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def _validate_coordinates(self, row: int, col: int) -> None:
        if self._in_bounds(row, col):
            return
        raise IndexError(
            f"Board coordinates out of range: row={row}, col={col}, "
            f"size={self.rows}x{self.cols}"
        )

    def _index(self, row: int, col: int) -> int:
        self._validate_coordinates(row, col)
        return row * self.cols + col

    def get(self, row: int, col: int) -> Mole:
        return self.moles[self._index(row, col)]

    def _replace_mole(self, idx: int, mole: Mole) -> "Board":
        new_moles = self.moles[:idx] + (mole,) + self.moles[idx + 1 :]
        return Board(rows=self.rows, cols=self.cols, moles=new_moles)

    def update(self, dt: float, visible_duration: float) -> "Board":
        new_moles = tuple(m.update(dt, visible_duration) for m in self.moles)
        return Board(rows=self.rows, cols=self.cols, moles=new_moles)

    def try_spawn(self) -> "Board":
        hidden_indices = [
            i for i, m in enumerate(self.moles) if m.state == MoleState.HIDDEN
        ]
        if not hidden_indices:
            return self
        idx = random.choice(hidden_indices)
        new_mole = self.moles[idx].spawn()
        return self._replace_mole(idx, new_mole)

    def try_whack(self, row: int, col: int) -> Tuple["Board", bool]:
        if not self._in_bounds(row, col):
            return self, False
        idx = self._index(row, col)
        mole = self.moles[idx]
        if not mole.is_whackable():
            return self, False
        new_mole = mole.whack()
        return self._replace_mole(idx, new_mole), True
