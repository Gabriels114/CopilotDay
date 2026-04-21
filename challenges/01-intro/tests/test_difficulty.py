"""Tests for Difficulty feature — Challenge 02."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from config import GameConfig, Difficulty, DIFFICULTIES, DIFFICULTY_SETTINGS
from game import GameState, Phase
from mole import Mole, MoleState
from board import Board


# ---------------------------------------------------------------------------
# Difficulty enum and settings
# ---------------------------------------------------------------------------

def test_difficulties_list_has_four_levels():
    assert len(DIFFICULTIES) == 4


def test_difficulty_settings_covers_all_levels():
    for diff in Difficulty:
        assert diff in DIFFICULTY_SETTINGS
        s = DIFFICULTY_SETTINGS[diff]
        assert "mole_visible_time" in s
        assert "mole_spawn_interval" in s
        assert "score_multiplier" in s


def test_difficulty_settings_values_decrease_with_harder():
    times = [DIFFICULTY_SETTINGS[d]["mole_visible_time"] for d in DIFFICULTIES]
    intervals = [DIFFICULTY_SETTINGS[d]["mole_spawn_interval"] for d in DIFFICULTIES]
    assert times == sorted(times, reverse=True), "Harder difficulty → shorter visible time"
    assert intervals == sorted(intervals, reverse=True), "Harder difficulty → shorter spawn interval"


def test_difficulty_multipliers_increase_with_harder():
    multipliers = [DIFFICULTY_SETTINGS[d]["score_multiplier"] for d in DIFFICULTIES]
    assert multipliers == sorted(multipliers), "Harder difficulty → higher score multiplier"


# ---------------------------------------------------------------------------
# GameConfig difficulty field and properties
# ---------------------------------------------------------------------------

def test_default_difficulty_is_medium():
    config = GameConfig()
    assert config.difficulty == Difficulty.MEDIUM


def test_score_multiplier_matches_difficulty_setting():
    for diff in Difficulty:
        config = GameConfig(difficulty=diff)
        assert config.score_multiplier == DIFFICULTY_SETTINGS[diff]["score_multiplier"]


def test_gameconfig_is_frozen_with_difficulty():
    config = GameConfig()
    with pytest.raises(Exception):
        config.difficulty = Difficulty.EASY


# ---------------------------------------------------------------------------
# next_difficulty / prev_difficulty cycling
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("start,expected_next", [
    (Difficulty.EASY,   Difficulty.MEDIUM),
    (Difficulty.MEDIUM, Difficulty.HARD),
    (Difficulty.HARD,   Difficulty.INSANE),
    (Difficulty.INSANE, Difficulty.EASY),   # wraps around
])
def test_next_difficulty_cycles(start, expected_next):
    config = GameConfig(difficulty=start)
    assert config.next_difficulty().difficulty == expected_next


@pytest.mark.parametrize("start,expected_prev", [
    (Difficulty.MEDIUM, Difficulty.EASY),
    (Difficulty.HARD,   Difficulty.MEDIUM),
    (Difficulty.INSANE, Difficulty.HARD),
    (Difficulty.EASY,   Difficulty.INSANE),  # wraps around
])
def test_prev_difficulty_cycles(start, expected_prev):
    config = GameConfig(difficulty=start)
    assert config.prev_difficulty().difficulty == expected_prev


def test_next_difficulty_updates_mole_timings():
    config = GameConfig(difficulty=Difficulty.EASY)
    harder = config.next_difficulty()
    assert harder.mole_visible_time == pytest.approx(
        DIFFICULTY_SETTINGS[Difficulty.MEDIUM]["mole_visible_time"]
    )
    assert harder.mole_spawn_interval == pytest.approx(
        DIFFICULTY_SETTINGS[Difficulty.MEDIUM]["mole_spawn_interval"]
    )


def test_next_difficulty_returns_new_instance():
    config = GameConfig()
    new_config = config.next_difficulty()
    assert new_config is not config


def test_next_difficulty_preserves_grid_and_duration():
    config = GameConfig(grid_size=4, game_duration=60)
    harder = config.next_difficulty()
    assert harder.grid_size == 4
    assert harder.game_duration == 60


# ---------------------------------------------------------------------------
# Score multiplier in game whack()
# ---------------------------------------------------------------------------

def _state_with_rising_mole(difficulty: Difficulty) -> GameState:
    config = GameConfig(difficulty=difficulty)
    state = GameState.menu(config).start()
    rising = Mole(state=MoleState.RISING, progress=0.5)
    moles = (rising,) + state.board.moles[1:]
    board = Board(rows=state.board.rows, cols=state.board.cols, moles=moles)
    return GameState(
        phase=state.phase, config=state.config, board=board,
        score=0, time_remaining=state.time_remaining, spawn_timer=0.0,
    )


@pytest.mark.parametrize("difficulty,expected_score", [
    (Difficulty.EASY,   1),
    (Difficulty.MEDIUM, 2),
    (Difficulty.HARD,   3),
    (Difficulty.INSANE, 5),
])
def test_whack_score_matches_multiplier(difficulty, expected_score):
    state = _state_with_rising_mole(difficulty)
    result = state.whack(0, 0)
    assert result.score == expected_score


def test_whack_miss_gives_zero_regardless_of_difficulty():
    for diff in Difficulty:
        state = GameState.menu(GameConfig(difficulty=diff)).start()
        result = state.whack(0, 0)
        assert result.score == 0
