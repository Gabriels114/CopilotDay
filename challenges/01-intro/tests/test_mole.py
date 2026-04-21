"""Tests for mole.py — Mole state machine and immutability."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from mole import Mole, MoleState, RISE_SPEED, FALL_SPEED, WHACK_FLASH_DURATION


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def hidden_mole() -> Mole:
    return Mole()


@pytest.fixture()
def rising_mole() -> Mole:
    return Mole(state=MoleState.RISING, progress=0.0)


@pytest.fixture()
def visible_mole() -> Mole:
    return Mole(state=MoleState.VISIBLE, progress=1.0, time_visible=0.0)


@pytest.fixture()
def falling_mole() -> Mole:
    return Mole(state=MoleState.FALLING, progress=0.8)


@pytest.fixture()
def whacked_mole() -> Mole:
    return Mole(state=MoleState.WHACKED, progress=0.5, whack_flash=WHACK_FLASH_DURATION)


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------

def test_initial_state_is_hidden(hidden_mole):
    assert hidden_mole.state == MoleState.HIDDEN


def test_initial_progress_is_zero(hidden_mole):
    assert hidden_mole.progress == 0.0


def test_initial_time_visible_is_zero(hidden_mole):
    assert hidden_mole.time_visible == 0.0


def test_initial_whack_flash_is_zero(hidden_mole):
    assert hidden_mole.whack_flash == 0.0


# ---------------------------------------------------------------------------
# spawn()
# ---------------------------------------------------------------------------

def test_spawn_returns_rising_state(hidden_mole):
    spawned = hidden_mole.spawn()
    assert spawned.state == MoleState.RISING


def test_spawn_resets_progress_to_zero(hidden_mole):
    spawned = hidden_mole.spawn()
    assert spawned.progress == 0.0


def test_spawn_resets_time_visible(hidden_mole):
    m = Mole(state=MoleState.HIDDEN, time_visible=3.0)
    spawned = m.spawn()
    assert spawned.time_visible == 0.0


def test_spawn_returns_new_instance(hidden_mole):
    spawned = hidden_mole.spawn()
    assert spawned is not hidden_mole


# ---------------------------------------------------------------------------
# update() — RISING state
# ---------------------------------------------------------------------------

def test_rising_progress_increases_by_rise_speed_times_dt(rising_mole):
    dt = 0.1
    updated = rising_mole.update(dt, visible_duration=1.5)
    expected = min(1.0, rising_mole.progress + RISE_SPEED * dt)
    assert updated.progress == pytest.approx(expected)


def test_rising_progress_clamped_at_one(rising_mole):
    # Large dt forces progress past 1.0
    updated = rising_mole.update(10.0, visible_duration=1.5)
    assert updated.progress == pytest.approx(1.0)


def test_rising_stays_rising_when_progress_below_one():
    mole = Mole(state=MoleState.RISING, progress=0.1)
    updated = mole.update(0.01, visible_duration=1.5)
    assert updated.state == MoleState.RISING


def test_rising_transitions_to_visible_when_progress_reaches_one():
    # progress close to 1.0 — a small dt will push it over
    mole = Mole(state=MoleState.RISING, progress=0.99)
    updated = mole.update(1.0, visible_duration=1.5)
    assert updated.state == MoleState.VISIBLE


def test_rising_transition_resets_time_visible():
    mole = Mole(state=MoleState.RISING, progress=0.99)
    updated = mole.update(1.0, visible_duration=1.5)
    assert updated.time_visible == 0.0


# ---------------------------------------------------------------------------
# update() — VISIBLE state
# ---------------------------------------------------------------------------

def test_visible_time_visible_increments(visible_mole):
    dt = 0.2
    updated = visible_mole.update(dt, visible_duration=2.0)
    assert updated.time_visible == pytest.approx(dt)


def test_visible_stays_visible_before_duration(visible_mole):
    updated = visible_mole.update(0.1, visible_duration=2.0)
    assert updated.state == MoleState.VISIBLE


def test_visible_transitions_to_falling_when_time_exceeds_duration():
    mole = Mole(state=MoleState.VISIBLE, progress=1.0, time_visible=1.3)
    updated = mole.update(0.2, visible_duration=1.4)
    assert updated.state == MoleState.FALLING


def test_visible_to_falling_keeps_progress_at_one():
    mole = Mole(state=MoleState.VISIBLE, progress=1.0, time_visible=1.3)
    updated = mole.update(0.2, visible_duration=1.4)
    assert updated.progress == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# update() — FALLING state
# ---------------------------------------------------------------------------

def test_falling_progress_decreases(falling_mole):
    dt = 0.1
    updated = falling_mole.update(dt, visible_duration=1.5)
    expected = max(0.0, falling_mole.progress - FALL_SPEED * dt)
    assert updated.progress == pytest.approx(expected)


def test_falling_stays_falling_when_progress_above_zero():
    mole = Mole(state=MoleState.FALLING, progress=0.9)
    updated = mole.update(0.01, visible_duration=1.5)
    assert updated.state == MoleState.FALLING


def test_falling_transitions_to_hidden_when_progress_reaches_zero():
    mole = Mole(state=MoleState.FALLING, progress=0.05)
    # dt large enough to bring progress to zero
    updated = mole.update(1.0, visible_duration=1.5)
    assert updated.state == MoleState.HIDDEN


def test_falling_to_hidden_resets_fields():
    mole = Mole(state=MoleState.FALLING, progress=0.05, time_visible=1.5, whack_flash=0.1)
    updated = mole.update(1.0, visible_duration=1.5)
    assert updated.progress == 0.0
    assert updated.time_visible == 0.0
    assert updated.whack_flash == 0.0


# ---------------------------------------------------------------------------
# update() — WHACKED state
# ---------------------------------------------------------------------------

def test_whacked_progress_decreases_faster_than_falling(whacked_mole):
    dt = 0.1
    updated = whacked_mole.update(dt, visible_duration=1.5)
    expected = max(0.0, whacked_mole.progress - FALL_SPEED * dt)
    assert updated.progress == pytest.approx(expected)


def test_whacked_flash_decreases(whacked_mole):
    dt = 0.1
    updated = whacked_mole.update(dt, visible_duration=1.5)
    expected_flash = max(0.0, whacked_mole.whack_flash - dt)
    assert updated.whack_flash == pytest.approx(expected_flash)


def test_whacked_transitions_to_hidden_when_progress_zero():
    mole = Mole(state=MoleState.WHACKED, progress=0.05, whack_flash=0.1)
    updated = mole.update(1.0, visible_duration=1.5)
    assert updated.state == MoleState.HIDDEN


def test_whacked_to_hidden_clears_all_fields():
    mole = Mole(state=MoleState.WHACKED, progress=0.05, time_visible=1.0, whack_flash=0.1)
    updated = mole.update(1.0, visible_duration=1.5)
    assert updated.progress == 0.0
    assert updated.whack_flash == 0.0


# ---------------------------------------------------------------------------
# update() — HIDDEN state (no-op)
# ---------------------------------------------------------------------------

def test_hidden_update_returns_same_mole(hidden_mole):
    updated = hidden_mole.update(0.5, visible_duration=1.5)
    assert updated is hidden_mole


# ---------------------------------------------------------------------------
# whack()
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("state", [MoleState.RISING, MoleState.VISIBLE])
def test_whack_on_whackable_state_sets_whacked(state):
    mole = Mole(state=state, progress=0.5)
    whacked = mole.whack()
    assert whacked.state == MoleState.WHACKED


@pytest.mark.parametrize("state", [MoleState.RISING, MoleState.VISIBLE])
def test_whack_sets_flash_duration(state):
    mole = Mole(state=state, progress=0.5)
    whacked = mole.whack()
    assert whacked.whack_flash == pytest.approx(WHACK_FLASH_DURATION)


@pytest.mark.parametrize("state", [MoleState.HIDDEN, MoleState.FALLING, MoleState.WHACKED])
def test_whack_on_non_whackable_returns_same_mole(state):
    mole = Mole(state=state, progress=0.5)
    result = mole.whack()
    assert result is mole


# ---------------------------------------------------------------------------
# is_whackable()
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("state,expected", [
    (MoleState.RISING, True),
    (MoleState.VISIBLE, True),
    (MoleState.HIDDEN, False),
    (MoleState.FALLING, False),
    (MoleState.WHACKED, False),
])
def test_is_whackable(state, expected):
    mole = Mole(state=state, progress=0.5)
    assert mole.is_whackable() == expected


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------

def test_mole_is_immutable(rising_mole):
    with pytest.raises(Exception):  # FrozenInstanceError is a subclass of AttributeError
        rising_mole.state = MoleState.VISIBLE  # type: ignore[misc]


def test_update_returns_new_instance(rising_mole):
    updated = rising_mole.update(0.1, visible_duration=1.5)
    assert updated is not rising_mole


def test_whack_returns_new_instance():
    mole = Mole(state=MoleState.RISING, progress=0.5)
    whacked = mole.whack()
    assert whacked is not mole


def test_spawn_does_not_mutate_original(hidden_mole):
    original_state = hidden_mole.state
    hidden_mole.spawn()
    assert hidden_mole.state == original_state
