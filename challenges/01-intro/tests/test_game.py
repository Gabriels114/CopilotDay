"""Tests for game.py — GameState phases, transitions, and immutability."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from config import GameConfig
from mole import Mole, MoleState
from board import Board
from game import GameState, Phase


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def default_config() -> GameConfig:
    return GameConfig(
        grid_size=3,
        game_duration=30,
        mole_visible_time=1.4,
        mole_spawn_interval=0.9,
    )


@pytest.fixture()
def menu_state(default_config) -> GameState:
    return GameState.menu(default_config)


@pytest.fixture()
def playing_state(menu_state) -> GameState:
    return menu_state.start()


@pytest.fixture()
def gameover_state(playing_state) -> GameState:
    # Fast-forward past the game duration
    return playing_state.update(playing_state.config.game_duration + 1.0)


# ---------------------------------------------------------------------------
# GameState.menu()
# ---------------------------------------------------------------------------

def test_menu_creates_menu_phase(menu_state):
    assert menu_state.phase == Phase.MENU


def test_menu_score_is_zero(menu_state):
    assert menu_state.score == 0


def test_menu_time_remaining_equals_game_duration(menu_state, default_config):
    assert menu_state.time_remaining == pytest.approx(float(default_config.game_duration))


def test_menu_spawn_timer_is_zero(menu_state):
    assert menu_state.spawn_timer == 0.0


def test_menu_board_matches_config_size(menu_state, default_config):
    expected_cells = default_config.grid_size ** 2
    assert len(menu_state.board.moles) == expected_cells


def test_menu_config_stored(menu_state, default_config):
    assert menu_state.config is default_config


# ---------------------------------------------------------------------------
# start()
# ---------------------------------------------------------------------------

def test_start_sets_playing_phase(playing_state):
    assert playing_state.phase == Phase.PLAYING


def test_start_score_is_zero(playing_state):
    assert playing_state.score == 0


def test_start_time_remaining_equals_game_duration(playing_state, default_config):
    assert playing_state.time_remaining == pytest.approx(float(default_config.game_duration))


def test_start_spawn_timer_is_zero(playing_state):
    assert playing_state.spawn_timer == 0.0


def test_start_creates_fresh_board(playing_state, default_config):
    assert all(m.state == MoleState.HIDDEN for m in playing_state.board.moles)


# ---------------------------------------------------------------------------
# update() — MENU phase
# ---------------------------------------------------------------------------

def test_menu_update_returns_same_state(menu_state):
    updated = menu_state.update(0.5)
    assert updated is menu_state


def test_menu_update_does_not_change_time_remaining(menu_state):
    updated = menu_state.update(0.5)
    assert updated.time_remaining == menu_state.time_remaining


# ---------------------------------------------------------------------------
# update() — PLAYING phase
# ---------------------------------------------------------------------------

def test_playing_update_decrements_time_remaining(playing_state):
    dt = 0.5
    updated = playing_state.update(dt)
    assert updated.time_remaining == pytest.approx(playing_state.time_remaining - dt)


def test_playing_update_returns_new_state(playing_state):
    updated = playing_state.update(0.1)
    assert updated is not playing_state


def test_playing_update_transitions_to_gameover_when_time_expires(playing_state):
    big_dt = playing_state.time_remaining + 1.0
    updated = playing_state.update(big_dt)
    assert updated.phase == Phase.GAMEOVER


def test_playing_update_gameover_time_remaining_is_zero(playing_state):
    updated = playing_state.update(playing_state.time_remaining + 1.0)
    assert updated.time_remaining == 0.0


def test_playing_update_increments_spawn_timer(playing_state):
    dt = 0.1
    # Ensure dt is small enough not to trigger a spawn reset
    state = GameState(
        phase=playing_state.phase,
        config=playing_state.config,
        board=playing_state.board,
        score=playing_state.score,
        time_remaining=playing_state.time_remaining,
        spawn_timer=0.0,
    )
    updated = state.update(dt)
    # spawn_timer < mole_spawn_interval, so it should have incremented
    if dt < state.config.mole_spawn_interval:
        assert updated.spawn_timer == pytest.approx(dt)


def test_playing_update_preserves_spawn_timer_excess_after_spawn(playing_state):
    # Set spawn_timer just below the threshold so a small dt triggers a spawn
    interval = playing_state.config.mole_spawn_interval
    state = GameState(
        phase=playing_state.phase,
        config=playing_state.config,
        board=playing_state.board,
        score=playing_state.score,
        time_remaining=playing_state.time_remaining,
        spawn_timer=interval - 0.01,
    )
    updated = state.update(0.02)
    assert updated.spawn_timer == pytest.approx(0.01)


def test_playing_update_spawns_mole_when_spawn_timer_exceeds_interval(playing_state):
    interval = playing_state.config.mole_spawn_interval
    state = GameState(
        phase=playing_state.phase,
        config=playing_state.config,
        board=playing_state.board,
        score=playing_state.score,
        time_remaining=playing_state.time_remaining,
        spawn_timer=interval - 0.01,
    )
    updated = state.update(0.02)
    rising_count = sum(1 for m in updated.board.moles if m.state == MoleState.RISING)
    assert rising_count == 1


# ---------------------------------------------------------------------------
# update() — GAMEOVER phase (no-op via propagation)
# ---------------------------------------------------------------------------

def test_gameover_update_keeps_gameover_phase(gameover_state):
    # update on gameover propagates through the playing logic — time_remaining is 0
    # and will immediately return GAMEOVER again
    updated = gameover_state.update(0.1)
    assert updated.phase == Phase.GAMEOVER


# ---------------------------------------------------------------------------
# whack()
# ---------------------------------------------------------------------------

def test_playing_whack_increments_score_on_hit(playing_state):
    # Manually insert a rising mole at (0,0)
    rising = Mole(state=MoleState.RISING, progress=0.5)
    moles = (rising,) + playing_state.board.moles[1:]
    board = Board(rows=playing_state.board.rows, cols=playing_state.board.cols, moles=moles)
    state = GameState(
        phase=playing_state.phase,
        config=playing_state.config,
        board=board,
        score=playing_state.score,
        time_remaining=playing_state.time_remaining,
        spawn_timer=playing_state.spawn_timer,
    )
    result = state.whack(0, 0)
    assert result.score == state.score + state.config.score_multiplier


def test_playing_whack_does_not_increment_score_on_miss(playing_state):
    # All moles hidden — whack any cell should be a miss
    result = playing_state.whack(0, 0)
    assert result.score == playing_state.score


def test_playing_whack_returns_new_state(playing_state):
    result = playing_state.whack(0, 0)
    assert result is not playing_state


@pytest.mark.parametrize("phase", [Phase.MENU, Phase.GAMEOVER])
def test_whack_outside_playing_is_no_op(menu_state, gameover_state, phase):
    state = menu_state if phase == Phase.MENU else gameover_state
    rising = Mole(state=MoleState.RISING, progress=0.5)
    board = Board(rows=state.board.rows, cols=state.board.cols, moles=(rising,) + state.board.moles[1:])
    guarded_state = GameState(
        phase=state.phase,
        config=state.config,
        board=board,
        score=state.score,
        time_remaining=state.time_remaining,
        spawn_timer=state.spawn_timer,
    )
    result = guarded_state.whack(0, 0)
    assert result is guarded_state
    assert result.score == guarded_state.score
    assert result.board is guarded_state.board


def test_playing_whack_out_of_bounds_is_safe_miss(playing_state):
    result = playing_state.whack(-1, 0)
    assert result.score == playing_state.score
    assert result.board is playing_state.board


# ---------------------------------------------------------------------------
# with_config()
# ---------------------------------------------------------------------------

def test_with_config_updates_config(menu_state):
    new_config = GameConfig(grid_size=4, game_duration=45)
    updated = menu_state.with_config(new_config)
    assert updated.config is new_config


def test_with_config_preserves_phase(menu_state):
    new_config = GameConfig(grid_size=4, game_duration=45)
    updated = menu_state.with_config(new_config)
    assert updated.phase == menu_state.phase


def test_with_config_preserves_score(menu_state):
    new_config = GameConfig(grid_size=4, game_duration=45)
    updated = menu_state.with_config(new_config)
    assert updated.score == menu_state.score


def test_with_config_creates_new_board_matching_new_size(menu_state):
    new_config = GameConfig(grid_size=4, game_duration=45)
    updated = menu_state.with_config(new_config)
    assert len(updated.board.moles) == 16


def test_with_config_returns_new_instance(menu_state):
    new_config = GameConfig(grid_size=5, game_duration=60)
    updated = menu_state.with_config(new_config)
    assert updated is not menu_state


def test_with_config_updates_time_remaining(menu_state):
    new_config = GameConfig(grid_size=3, game_duration=60)
    updated = menu_state.with_config(new_config)
    assert updated.time_remaining == pytest.approx(60.0)


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------

def test_game_state_is_frozen(playing_state):
    with pytest.raises(Exception):
        playing_state.score = 999  # type: ignore[misc]


def test_update_does_not_mutate_original(playing_state):
    original_time = playing_state.time_remaining
    original_score = playing_state.score
    playing_state.update(0.5)
    assert playing_state.time_remaining == original_time
    assert playing_state.score == original_score


def test_whack_does_not_mutate_original(playing_state):
    # Insert a rising mole
    rising = Mole(state=MoleState.RISING, progress=0.5)
    moles = (rising,) + playing_state.board.moles[1:]
    board = Board(rows=playing_state.board.rows, cols=playing_state.board.cols, moles=moles)
    state = GameState(
        phase=playing_state.phase,
        config=playing_state.config,
        board=board,
        score=0,
        time_remaining=playing_state.time_remaining,
        spawn_timer=playing_state.spawn_timer,
    )
    state.whack(0, 0)
    assert state.score == 0
    assert state.board.get(0, 0).state == MoleState.RISING
