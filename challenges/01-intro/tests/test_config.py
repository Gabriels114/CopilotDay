"""Tests for config.py — GameConfig defaults, cycling methods, and immutability."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from dataclasses import FrozenInstanceError
from config import GameConfig, GRID_SIZES, DURATIONS


# ---------------------------------------------------------------------------
# Default values
# ---------------------------------------------------------------------------

def test_default_grid_size():
    config = GameConfig()
    assert config.grid_size == 3


def test_default_game_duration():
    config = GameConfig()
    assert config.game_duration == 30


def test_default_mole_visible_time():
    config = GameConfig()
    assert config.mole_visible_time == pytest.approx(1.4)


def test_default_mole_spawn_interval():
    config = GameConfig()
    assert config.mole_spawn_interval == pytest.approx(0.9)


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------

def test_grid_rows_equals_grid_size():
    config = GameConfig(grid_size=4)
    assert config.grid_rows == 4


def test_grid_cols_equals_grid_size():
    config = GameConfig(grid_size=5)
    assert config.grid_cols == 5


def test_grid_rows_and_cols_equal_each_other():
    config = GameConfig(grid_size=3)
    assert config.grid_rows == config.grid_cols


@pytest.mark.parametrize("size", GRID_SIZES)
def test_grid_rows_for_all_valid_sizes(size):
    config = GameConfig(grid_size=size)
    assert config.grid_rows == size


@pytest.mark.parametrize("size", GRID_SIZES)
def test_grid_cols_for_all_valid_sizes(size):
    config = GameConfig(grid_size=size)
    assert config.grid_cols == size


# ---------------------------------------------------------------------------
# next_size()
# ---------------------------------------------------------------------------

def test_next_size_from_3_returns_4():
    config = GameConfig(grid_size=3)
    assert config.next_size().grid_size == 4


def test_next_size_from_4_returns_5():
    config = GameConfig(grid_size=4)
    assert config.next_size().grid_size == 5


def test_next_size_from_5_wraps_to_3():
    config = GameConfig(grid_size=5)
    assert config.next_size().grid_size == 3


def test_next_size_cycles_through_all():
    config = GameConfig(grid_size=GRID_SIZES[0])
    sizes_seen = []
    for _ in range(len(GRID_SIZES)):
        config = config.next_size()
        sizes_seen.append(config.grid_size)
    assert sizes_seen == GRID_SIZES[1:] + [GRID_SIZES[0]]


def test_next_size_preserves_other_fields():
    config = GameConfig(grid_size=3, game_duration=45, mole_visible_time=2.0, mole_spawn_interval=1.0)
    updated = config.next_size()
    assert updated.game_duration == 45
    assert updated.mole_visible_time == pytest.approx(2.0)
    assert updated.mole_spawn_interval == pytest.approx(1.0)


def test_next_size_returns_new_instance():
    config = GameConfig(grid_size=3)
    assert config.next_size() is not config


# ---------------------------------------------------------------------------
# prev_size()
# ---------------------------------------------------------------------------

def test_prev_size_from_5_returns_4():
    config = GameConfig(grid_size=5)
    assert config.prev_size().grid_size == 4


def test_prev_size_from_4_returns_3():
    config = GameConfig(grid_size=4)
    assert config.prev_size().grid_size == 3


def test_prev_size_from_3_wraps_to_5():
    config = GameConfig(grid_size=3)
    assert config.prev_size().grid_size == 5


def test_prev_size_is_inverse_of_next_size():
    config = GameConfig(grid_size=4)
    assert config.next_size().prev_size().grid_size == config.grid_size


def test_prev_size_preserves_other_fields():
    config = GameConfig(grid_size=5, game_duration=60)
    updated = config.prev_size()
    assert updated.game_duration == 60


# ---------------------------------------------------------------------------
# next_duration()
# ---------------------------------------------------------------------------

def test_next_duration_from_15_returns_30():
    config = GameConfig(game_duration=15)
    assert config.next_duration().game_duration == 30


def test_next_duration_from_30_returns_45():
    config = GameConfig(game_duration=30)
    assert config.next_duration().game_duration == 45


def test_next_duration_from_45_returns_60():
    config = GameConfig(game_duration=45)
    assert config.next_duration().game_duration == 60


def test_next_duration_from_60_returns_90():
    config = GameConfig(game_duration=60)
    assert config.next_duration().game_duration == 90


def test_next_duration_from_90_wraps_to_15():
    config = GameConfig(game_duration=90)
    assert config.next_duration().game_duration == 15


def test_next_duration_cycles_through_all():
    config = GameConfig(game_duration=DURATIONS[0])
    durations_seen = []
    for _ in range(len(DURATIONS)):
        config = config.next_duration()
        durations_seen.append(config.game_duration)
    assert durations_seen == DURATIONS[1:] + [DURATIONS[0]]


def test_next_duration_preserves_grid_size():
    config = GameConfig(grid_size=5, game_duration=30)
    updated = config.next_duration()
    assert updated.grid_size == 5


def test_next_duration_returns_new_instance():
    config = GameConfig(game_duration=30)
    assert config.next_duration() is not config


# ---------------------------------------------------------------------------
# prev_duration()
# ---------------------------------------------------------------------------

def test_prev_duration_from_90_returns_60():
    config = GameConfig(game_duration=90)
    assert config.prev_duration().game_duration == 60


def test_prev_duration_from_15_wraps_to_90():
    config = GameConfig(game_duration=15)
    assert config.prev_duration().game_duration == 90


def test_prev_duration_is_inverse_of_next_duration():
    config = GameConfig(game_duration=45)
    assert config.next_duration().prev_duration().game_duration == config.game_duration


def test_prev_duration_preserves_grid_size():
    config = GameConfig(grid_size=4, game_duration=60)
    updated = config.prev_duration()
    assert updated.grid_size == 4


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------

def test_game_config_is_frozen():
    config = GameConfig()
    with pytest.raises(FrozenInstanceError):
        config.grid_size = 5  # type: ignore[misc]


def test_game_config_duration_frozen():
    config = GameConfig()
    with pytest.raises(FrozenInstanceError):
        config.game_duration = 90  # type: ignore[misc]


def test_next_size_does_not_mutate_original():
    config = GameConfig(grid_size=3)
    config.next_size()
    assert config.grid_size == 3


def test_next_duration_does_not_mutate_original():
    config = GameConfig(game_duration=30)
    config.next_duration()
    assert config.game_duration == 30
