"""Tests for board.py — Board creation, updates, spawning, and whacking."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from mole import Mole, MoleState
from board import Board


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def all_hidden(board: Board) -> bool:
    return all(m.state == MoleState.HIDDEN for m in board.moles)


def make_full_board(rows: int = 3, cols: int = 3) -> Board:
    """Return a board where every mole is VISIBLE (non-HIDDEN)."""
    moles = tuple(
        Mole(state=MoleState.VISIBLE, progress=1.0) for _ in range(rows * cols)
    )
    return Board(rows=rows, cols=cols, moles=moles)


# ---------------------------------------------------------------------------
# Board.create()
# ---------------------------------------------------------------------------


def test_create_3x3_has_nine_moles():
    board = Board.create(3, 3)
    assert len(board.moles) == 9


def test_create_4x4_has_sixteen_moles():
    board = Board.create(4, 4)
    assert len(board.moles) == 16


def test_create_5x5_has_twenty_five_moles():
    board = Board.create(5, 5)
    assert len(board.moles) == 25


def test_create_all_moles_hidden():
    board = Board.create(3, 3)
    assert all_hidden(board)


def test_create_stores_correct_rows_and_cols():
    board = Board.create(4, 5)
    assert board.rows == 4
    assert board.cols == 5


# ---------------------------------------------------------------------------
# get(row, col)
# ---------------------------------------------------------------------------


def test_get_returns_correct_mole_by_index():
    moles = tuple(
        Mole(state=MoleState.VISIBLE if i == 4 else MoleState.HIDDEN) for i in range(9)
    )
    board = Board(rows=3, cols=3, moles=moles)
    # index 4 = row 1, col 1
    assert board.get(1, 1).state == MoleState.VISIBLE


def test_get_first_mole():
    board = Board.create(3, 3)
    assert board.get(0, 0) is board.moles[0]


def test_get_last_mole():
    board = Board.create(3, 3)
    assert board.get(2, 2) is board.moles[8]


def test_get_uses_row_col_formula():
    board = Board.create(4, 4)
    for r in range(4):
        for c in range(4):
            assert board.get(r, c) is board.moles[r * 4 + c]


@pytest.mark.parametrize(
    ("row", "col"),
    [(-1, 0), (0, -1), (3, 0), (0, 3)],
)
def test_get_rejects_out_of_bounds_coordinates(row, col):
    board = Board.create(3, 3)
    with pytest.raises(IndexError):
        board.get(row, col)


# ---------------------------------------------------------------------------
# update()
# ---------------------------------------------------------------------------


def test_update_propagates_to_all_moles():
    # Put a rising mole in position 0; after update its progress should grow
    rising = Mole(state=MoleState.RISING, progress=0.0)
    moles = (rising,) + tuple(Mole() for _ in range(8))
    board = Board(rows=3, cols=3, moles=moles)
    updated = board.update(0.1, visible_duration=1.5)
    assert updated.moles[0].progress > 0.0


def test_update_returns_new_board():
    board = Board.create(3, 3)
    updated = board.update(0.1, visible_duration=1.5)
    assert updated is not board


def test_update_does_not_change_hidden_moles():
    board = Board.create(3, 3)
    updated = board.update(0.1, visible_duration=1.5)
    for mole in updated.moles:
        assert mole.state == MoleState.HIDDEN


def test_update_preserves_rows_and_cols():
    board = Board.create(4, 4)
    updated = board.update(0.1, visible_duration=1.5)
    assert updated.rows == 4
    assert updated.cols == 4


# ---------------------------------------------------------------------------
# try_spawn()
# ---------------------------------------------------------------------------


def test_try_spawn_changes_exactly_one_hidden_to_rising():
    board = Board.create(3, 3)
    spawned = board.try_spawn()
    rising_count = sum(1 for m in spawned.moles if m.state == MoleState.RISING)
    assert rising_count == 1


def test_try_spawn_chosen_mole_was_hidden():
    board = Board.create(3, 3)
    spawned = board.try_spawn()
    # The spawned board should have exactly one RISING mole and the rest HIDDEN
    hidden_count = sum(1 for m in spawned.moles if m.state == MoleState.HIDDEN)
    assert hidden_count == 8


def test_try_spawn_on_full_board_returns_same_board():
    board = make_full_board(3, 3)
    result = board.try_spawn()
    assert result is board


def test_try_spawn_returns_new_board_when_spawn_succeeds():
    board = Board.create(3, 3)
    result = board.try_spawn()
    assert result is not board


def test_try_spawn_always_picks_hidden_mole():
    """Repeated spawns always pick a HIDDEN mole — never a non-HIDDEN one."""
    for _ in range(20):
        board = Board.create(3, 3)
        spawned = board.try_spawn()
        non_hidden_before = sum(1 for m in board.moles if m.state != MoleState.HIDDEN)
        non_hidden_after = sum(1 for m in spawned.moles if m.state != MoleState.HIDDEN)
        # Exactly one more non-hidden mole than before
        assert non_hidden_after == non_hidden_before + 1


def test_try_spawn_randomness_covers_different_positions():
    """Over many calls, more than one distinct index should be spawned."""
    spawned_indices = set()
    for _ in range(50):
        board = Board.create(3, 3)
        result = board.try_spawn()
        for i, mole in enumerate(result.moles):
            if mole.state == MoleState.RISING:
                spawned_indices.add(i)
    assert len(spawned_indices) > 1


# ---------------------------------------------------------------------------
# try_whack()
# ---------------------------------------------------------------------------


def test_try_whack_on_whackable_returns_true():
    rising = Mole(state=MoleState.RISING, progress=0.5)
    moles = (rising,) + tuple(Mole() for _ in range(8))
    board = Board(rows=3, cols=3, moles=moles)
    _, hit = board.try_whack(0, 0)
    assert hit is True


def test_try_whack_on_whackable_sets_mole_to_whacked():
    rising = Mole(state=MoleState.RISING, progress=0.5)
    moles = (rising,) + tuple(Mole() for _ in range(8))
    board = Board(rows=3, cols=3, moles=moles)
    new_board, _ = board.try_whack(0, 0)
    assert new_board.get(0, 0).state == MoleState.WHACKED


def test_try_whack_on_non_whackable_returns_false():
    board = Board.create(3, 3)  # all HIDDEN
    _, hit = board.try_whack(1, 1)
    assert hit is False


def test_try_whack_on_non_whackable_returns_same_board():
    board = Board.create(3, 3)
    result_board, _ = board.try_whack(1, 1)
    assert result_board is board


def test_try_whack_on_visible_mole_returns_true():
    visible = Mole(state=MoleState.VISIBLE, progress=1.0)
    moles = (
        tuple(Mole() for _ in range(4)) + (visible,) + tuple(Mole() for _ in range(4))
    )
    board = Board(rows=3, cols=3, moles=moles)
    _, hit = board.try_whack(1, 1)
    assert hit is True


def test_try_whack_does_not_affect_other_moles():
    rising = Mole(state=MoleState.RISING, progress=0.5)
    moles = (rising,) + tuple(Mole() for _ in range(8))
    board = Board(rows=3, cols=3, moles=moles)
    new_board, _ = board.try_whack(0, 0)
    for i in range(1, 9):
        assert new_board.moles[i].state == MoleState.HIDDEN


@pytest.mark.parametrize(
    ("row", "col"),
    [(-1, 0), (0, -1), (3, 0), (0, 3)],
)
def test_try_whack_out_of_bounds_returns_miss_and_same_board(row, col):
    board = Board.create(3, 3)
    new_board, hit = board.try_whack(row, col)
    assert new_board is board
    assert hit is False


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


def test_board_is_immutable():
    board = Board.create(3, 3)
    with pytest.raises(Exception):
        board.rows = 5  # type: ignore[misc]


def test_try_whack_returns_new_board_on_hit():
    rising = Mole(state=MoleState.RISING, progress=0.5)
    moles = (rising,) + tuple(Mole() for _ in range(8))
    board = Board(rows=3, cols=3, moles=moles)
    new_board, _ = board.try_whack(0, 0)
    assert new_board is not board


def test_try_whack_original_board_unchanged():
    rising = Mole(state=MoleState.RISING, progress=0.5)
    moles = (rising,) + tuple(Mole() for _ in range(8))
    board = Board(rows=3, cols=3, moles=moles)
    board.try_whack(0, 0)
    # Original board's mole at (0,0) must still be RISING
    assert board.get(0, 0).state == MoleState.RISING


def test_update_original_board_unchanged():
    board = Board.create(3, 3)
    original_moles = board.moles
    board.update(10.0, visible_duration=1.5)
    assert board.moles == original_moles
