import pygame
import pytest

from board import Board
from config import COLORS, GameConfig
from game import GameState, Phase
from mole import Mole, MoleState
import renderer


class DummyFont:
    def __init__(self):
        self.calls = []

    def render(self, text, antialias, color):
        self.calls.append((text, antialias, color))
        width = max(1, len(text) * 8)
        surface = pygame.Surface((width, 24), pygame.SRCALPHA)
        surface.fill(color)
        return surface


def _surface_bytes(surface):
    return pygame.image.tostring(surface, "RGBA")


def _make_state(time_remaining=15.0):
    config = GameConfig(grid_size=3, game_duration=30)
    board = Board(
        rows=3,
        cols=3,
        moles=(
            Mole(MoleState.HIDDEN, 0.0, 0.0, 0.0),
            Mole(MoleState.VISIBLE, 1.0, 0.4, 0.0),
            Mole(MoleState.WHACKED, 0.7, 0.0, 0.3),
            Mole(),
            Mole(),
            Mole(),
            Mole(),
            Mole(),
            Mole(),
        ),
    )
    return GameState(
        phase=Phase.PLAYING,
        config=config,
        board=board,
        score=7,
        time_remaining=time_remaining,
        spawn_timer=0.0,
    )


def test_compute_layout_centers_grid():
    config = GameConfig(grid_size=4)
    cell_size, offset_x, offset_y = renderer.compute_layout(config)

    assert cell_size == min(renderer.WINDOW_W // 4, (renderer.WINDOW_H - renderer.HUD_H) // 4)
    assert offset_x >= 0
    assert offset_y >= renderer.HUD_H


def test_pixel_to_cell_maps_inside_and_outside_positions():
    config = GameConfig(grid_size=3)
    cell_size, offset_x, offset_y = renderer.compute_layout(config)

    assert renderer.pixel_to_cell(offset_x + 1, offset_y + 1, config, cell_size, offset_x, offset_y) == (0, 0)
    assert renderer.pixel_to_cell(offset_x - 5, offset_y, config, cell_size, offset_x, offset_y) is None
    assert renderer.pixel_to_cell(offset_x, offset_y + (cell_size * config.grid_rows), config, cell_size, offset_x, offset_y) is None


def test_draw_background_applies_gradient(screen_surface):
    renderer.draw_background(screen_surface)

    assert screen_surface.get_at((0, 0))[:3] == COLORS["bg_top"]
    assert screen_surface.get_at((0, renderer.WINDOW_H - 1))[:3] != COLORS["bg_top"]


def test_private_drawing_helpers_modify_surface(screen_surface):
    before = _surface_bytes(screen_surface)
    renderer._draw_hole(screen_surface, 100, 120, 30, 18)
    assert _surface_bytes(screen_surface) != before

    normal_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    whacked_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    renderer._draw_mole_head(normal_surface, 100, 100, 30, False, 0.0)
    renderer._draw_mole_head(whacked_surface, 100, 100, 30, True, 0.3)

    assert _surface_bytes(normal_surface) != _surface_bytes(whacked_surface)

    rays_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    before = _surface_bytes(rays_surface)
    renderer._draw_x_eye(rays_surface, 70, 70, 8)
    renderer._draw_whack_rays(rays_surface, 100, 100, 20)
    assert _surface_bytes(rays_surface) != before


@pytest.mark.parametrize(
    ("mole", "center"),
    [
        (Mole(MoleState.HIDDEN, 0.0, 0.0, 0.0), (100, 100)),
        (Mole(MoleState.VISIBLE, 1.0, 0.2, 0.0), (220, 100)),
        (Mole(MoleState.WHACKED, 0.8, 0.0, 0.3), (340, 100)),
    ],
)
def test_draw_cell_preserves_clip_and_draws_expected_content(screen_surface, mole, center):
    old_clip = screen_surface.get_clip()
    before = _surface_bytes(screen_surface)

    renderer._draw_cell(screen_surface, center[0], center[1], 100, mole)

    assert screen_surface.get_clip() == old_clip
    if mole.state == MoleState.HIDDEN:
        assert _surface_bytes(screen_surface) != before
    else:
        assert screen_surface.get_at(center) != pygame.Color(0, 0, 0, 0)


def test_draw_grid_renders_board(screen_surface):
    state = _make_state()
    before = _surface_bytes(screen_surface)

    renderer.draw_grid(screen_surface, state)

    assert _surface_bytes(screen_surface) != before


@pytest.mark.parametrize(
    ("time_remaining", "expected_color"),
    [
        (20.0, COLORS["timer_ok"]),
        (10.0, COLORS["timer_warn"]),
        (3.0, COLORS["timer_low"]),
    ],
)
def test_draw_hud_uses_timer_threshold_colors(screen_surface, time_remaining, expected_color):
    state = _make_state(time_remaining=time_remaining)
    large_font = DummyFont()
    medium_font = DummyFont()

    renderer.draw_hud(screen_surface, state, large_font, medium_font)

    assert large_font.calls[0][0] == f"Score: {state.score}"
    assert large_font.calls[1][0] == f"Time: {int(-(-state.time_remaining // 1))}s"
    assert large_font.calls[1][2] == expected_color


def test_draw_button_changes_color_on_hover(screen_surface):
    font = DummyFont()
    rect = pygame.Rect(20, 20, 120, 50)

    renderer._draw_button(screen_surface, rect, "PLAY", font, (0, 0))
    normal_color = screen_surface.get_at((rect.x + 5, rect.y + 5))[:3]

    hovered_surface = pygame.Surface((200, 120), pygame.SRCALPHA)
    renderer._draw_button(hovered_surface, rect, "PLAY", font, rect.center)
    hovered_color = hovered_surface.get_at((rect.x + 5, rect.y + 5))[:3]

    assert normal_color == COLORS["btn_normal"]
    assert hovered_color == COLORS["btn_hover"]


def test_draw_menu_returns_all_controls(screen_surface):
    state = GameState.menu(GameConfig(grid_size=4, game_duration=45))
    title_font = DummyFont()
    large_font = DummyFont()
    medium_font = DummyFont()
    before = _surface_bytes(screen_surface)

    rects = renderer.draw_menu(screen_surface, state, title_font, large_font, medium_font, (0, 0))

    assert set(rects) == {
        "prev_size",
        "next_size",
        "prev_dur",
        "next_dur",
        "prev_diff",
        "next_diff",
        "play",
    }
    assert all(isinstance(rect, pygame.Rect) for rect in rects.values())
    assert _surface_bytes(screen_surface) != before


def test_draw_gameover_returns_expected_buttons(screen_surface):
    state = _make_state(time_remaining=0.0)
    title_font = DummyFont()
    large_font = DummyFont()
    medium_font = DummyFont()
    before = _surface_bytes(screen_surface)

    rects = renderer.draw_gameover(screen_surface, state, 11, title_font, large_font, medium_font, (0, 0))

    assert set(rects) == {"play_again", "menu"}
    assert rects["play_again"].width > 0
    assert rects["menu"].width > 0
    assert _surface_bytes(screen_surface) != before
