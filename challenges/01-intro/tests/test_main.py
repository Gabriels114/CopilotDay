import pygame

from config import Difficulty, GameConfig
from game import GameState, Phase
import main as app_main


class FakeClock:
    def __init__(self, ticks):
        self._ticks = iter(ticks)

    def tick(self, fps):
        return next(self._ticks)


def _mouse_event(pos):
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos)


def test_load_font_uses_fallback_when_sysfont_fails(monkeypatch):
    calls = []

    def fake_sysfont(name, size, bold=False):
        calls.append((name, size, bold))
        raise pygame.error("missing font")

    monkeypatch.setattr(pygame.font, "SysFont", fake_sysfont)

    font = app_main._load_font(28, bold=True)

    assert isinstance(font, pygame.font.Font)
    assert calls


def test_load_font_uses_sysfont_when_available():
    font = app_main._load_font(22)

    assert isinstance(font, pygame.font.Font)


def test_handle_menu_click_routes_buttons():
    initial = GameState.menu(GameConfig(grid_size=4, game_duration=45))
    rects = {
        "prev_size": pygame.Rect(0, 0, 20, 20),
        "next_size": pygame.Rect(30, 0, 20, 20),
        "prev_dur": pygame.Rect(60, 0, 20, 20),
        "next_dur": pygame.Rect(90, 0, 20, 20),
        "prev_diff": pygame.Rect(120, 0, 20, 20),
        "next_diff": pygame.Rect(150, 0, 20, 20),
        "play": pygame.Rect(180, 0, 20, 20),
    }

    assert app_main._handle_menu_click(initial, rects["prev_size"].center, rects).config.grid_size == 3
    assert app_main._handle_menu_click(initial, rects["next_size"].center, rects).config.grid_size == 5
    assert app_main._handle_menu_click(initial, rects["prev_dur"].center, rects).config.game_duration == 30
    assert app_main._handle_menu_click(initial, rects["next_dur"].center, rects).config.game_duration == 60
    assert app_main._handle_menu_click(initial, rects["prev_diff"].center, rects).config.difficulty == Difficulty.EASY
    assert app_main._handle_menu_click(initial, rects["next_diff"].center, rects).config.difficulty == Difficulty.HARD
    assert app_main._handle_menu_click(initial, rects["play"].center, rects).phase == Phase.PLAYING
    assert app_main._handle_menu_click(initial, (999, 999), rects) is initial


def test_handle_gameover_click_routes_buttons():
    state = GameState.menu(GameConfig()).start().update(31.0)
    rects = {
        "play_again": pygame.Rect(0, 0, 20, 20),
        "menu": pygame.Rect(30, 0, 20, 20),
    }

    assert app_main._handle_gameover_click(state, rects["play_again"].center, rects).phase == Phase.PLAYING
    assert app_main._handle_gameover_click(state, rects["menu"].center, rects).phase == Phase.MENU
    assert app_main._handle_gameover_click(state, (999, 999), rects) is state


def test_main_runs_menu_to_gameover_and_back(monkeypatch):
    screen = pygame.Surface((app_main.WINDOW_W, app_main.WINDOW_H), pygame.SRCALPHA)
    font = pygame.font.Font(None, 24)
    play_rect = pygame.Rect(100, 100, 80, 40)
    menu_rect = pygame.Rect(100, 200, 80, 40)
    calls = {"background": 0, "menu": 0, "grid": 0, "hud": 0, "gameover": []}
    events = iter([
        [],
        [_mouse_event(play_rect.center)],
        [_mouse_event(menu_rect.center)],
        [pygame.event.Event(pygame.QUIT)],
    ])

    monkeypatch.setattr(pygame.display, "set_mode", lambda size: screen)
    monkeypatch.setattr(pygame.display, "set_caption", lambda title: None)
    monkeypatch.setattr(pygame.display, "flip", lambda: None)
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (0, 0))
    monkeypatch.setattr(pygame.time, "Clock", lambda: FakeClock([0, 31_000, 0, 0]))
    monkeypatch.setattr(pygame.event, "get", lambda: next(events))
    monkeypatch.setattr(pygame, "quit", lambda: None)
    monkeypatch.setattr(app_main, "_load_font", lambda size, bold=False: font)

    def fake_draw_background(surface):
        calls["background"] += 1

    def fake_draw_menu(surface, state, font_title, font_large, font_medium, mouse_pos):
        calls["menu"] += 1
        return {"play": play_rect}

    def fake_draw_grid(surface, state):
        calls["grid"] += 1

    def fake_draw_hud(surface, state, font_large, font_medium):
        calls["hud"] += 1

    def fake_draw_gameover(surface, state, high_score, font_title, font_large, font_medium, mouse_pos):
        calls["gameover"].append((state.phase, high_score))
        return {"menu": menu_rect}

    monkeypatch.setattr(app_main, "draw_background", fake_draw_background)
    monkeypatch.setattr(app_main, "draw_menu", fake_draw_menu)
    monkeypatch.setattr(app_main, "draw_grid", fake_draw_grid)
    monkeypatch.setattr(app_main, "draw_hud", fake_draw_hud)
    monkeypatch.setattr(app_main, "draw_gameover", fake_draw_gameover)

    app_main.main()

    assert calls["background"] == 4
    assert calls["menu"] >= 2
    assert calls["grid"] >= 1
    assert calls["hud"] >= 1
    assert calls["gameover"] == [(Phase.GAMEOVER, 0)]


def test_main_whacks_clicked_cell_during_play(monkeypatch):
    pygame.font.init()
    screen = pygame.Surface((app_main.WINDOW_W, app_main.WINDOW_H), pygame.SRCALPHA)
    font = pygame.font.Font(None, 24)
    play_rect = pygame.Rect(100, 100, 80, 40)
    whack_calls = []
    events = iter([
        [],
        [_mouse_event(play_rect.center)],
        [_mouse_event((300, 300))],
        [pygame.event.Event(pygame.QUIT)],
    ])

    monkeypatch.setattr(pygame.display, "set_mode", lambda size: screen)
    monkeypatch.setattr(pygame.display, "set_caption", lambda title: None)
    monkeypatch.setattr(pygame.display, "flip", lambda: None)
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (0, 0))
    monkeypatch.setattr(pygame.time, "Clock", lambda: FakeClock([0, 0, 0, 0]))
    monkeypatch.setattr(pygame.event, "get", lambda: next(events))
    monkeypatch.setattr(pygame, "quit", lambda: None)
    monkeypatch.setattr(app_main, "_load_font", lambda size, bold=False: font)
    monkeypatch.setattr(app_main, "draw_background", lambda surface: None)
    monkeypatch.setattr(app_main, "draw_grid", lambda surface, state: None)
    monkeypatch.setattr(app_main, "draw_hud", lambda surface, state, font_large, font_medium: None)
    monkeypatch.setattr(app_main, "draw_gameover", lambda *args, **kwargs: {})
    monkeypatch.setattr(app_main, "compute_layout", lambda config: (90, 10, 100))
    monkeypatch.setattr(app_main, "pixel_to_cell", lambda px, py, config, cell_size, ox, oy: (1, 2))

    def fake_draw_menu(surface, state, font_title, font_large, font_medium, mouse_pos):
        return {"play": play_rect}

    def fake_whack(self, row, col):
        whack_calls.append((row, col))
        return self

    monkeypatch.setattr(app_main, "draw_menu", fake_draw_menu)
    monkeypatch.setattr(app_main.GameState, "whack", fake_whack)

    app_main.main()

    assert whack_calls == [(1, 2)]
