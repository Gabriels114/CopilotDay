import math
from typing import Dict, Optional, Tuple

import pygame

from config import COLORS, DIFFICULTY_COLORS, GameConfig
from mole import MoleState

WINDOW_W = 800
WINDOW_H = 700
HUD_H = 90
FPS = 60

_PLAY_AREA_H = WINDOW_H - HUD_H


def compute_layout(config: GameConfig) -> Tuple[int, int, int]:
    cell_w = WINDOW_W // config.grid_cols
    cell_h = _PLAY_AREA_H // config.grid_rows
    cell_size = min(cell_w, cell_h)
    total_w = cell_size * config.grid_cols
    total_h = cell_size * config.grid_rows
    offset_x = (WINDOW_W - total_w) // 2
    offset_y = HUD_H + (_PLAY_AREA_H - total_h) // 2
    return cell_size, offset_x, offset_y


def pixel_to_cell(
    px: int, py: int,
    config: GameConfig,
    cell_size: int,
    ox: int, oy: int,
) -> Optional[Tuple[int, int]]:
    col = (px - ox) // cell_size
    row = (py - oy) // cell_size
    if 0 <= row < config.grid_rows and 0 <= col < config.grid_cols:
        return row, col
    return None


def draw_background(surface: pygame.Surface) -> None:
    top = COLORS["bg_top"]
    bot = COLORS["bg_bottom"]
    h = WINDOW_H
    for y in range(h):
        t = y / h
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (WINDOW_W, y))


def _draw_hole(surface: pygame.Surface, cx: int, cy: int, hole_rx: int, hole_ry: int) -> None:
    pygame.draw.ellipse(surface, COLORS["hole_back"],
                        (cx - hole_rx, cy - hole_ry, hole_rx * 2, hole_ry * 2))
    rim_rect = (cx - hole_rx, cy - hole_ry // 2, hole_rx * 2, hole_ry)
    pygame.draw.ellipse(surface, COLORS["hole_rim"], rim_rect)
    dirt_rect = (cx - hole_rx - 6, cy - hole_ry - 4, (hole_rx + 6) * 2, (hole_ry + 4) * 2)
    pygame.draw.ellipse(surface, COLORS["dirt"], dirt_rect, 5)


def _draw_mole_head(
    surface: pygame.Surface,
    mx: int, my: int,
    radius: int,
    whacked: bool,
    flash: float,
) -> None:
    body_color = COLORS["whacked"] if (whacked and flash > 0) else COLORS["mole_body"]
    ear_color = COLORS["mole_ear"]
    ear_r = max(4, radius // 4)
    inner_ear_r = max(2, ear_r // 2)

    left_ear_x = mx - radius // 2
    right_ear_x = mx + radius // 2
    ear_y = my - radius + ear_r // 2

    pygame.draw.circle(surface, ear_color, (left_ear_x, ear_y), ear_r)
    pygame.draw.circle(surface, COLORS["mole_nose"], (left_ear_x, ear_y), inner_ear_r)
    pygame.draw.circle(surface, ear_color, (right_ear_x, ear_y), ear_r)
    pygame.draw.circle(surface, COLORS["mole_nose"], (right_ear_x, ear_y), inner_ear_r)

    pygame.draw.circle(surface, body_color, (mx, my), radius)

    shine_x = mx - radius // 4
    shine_y = my - radius // 3
    shine_r = max(3, radius // 6)
    pygame.draw.circle(surface, COLORS["mole_shine"], (shine_x, shine_y), shine_r)

    eye_offset_x = radius // 3
    eye_offset_y = radius // 6
    eye_r = max(3, radius // 7)

    if whacked:
        _draw_x_eye(surface, mx - eye_offset_x, my - eye_offset_y, eye_r)
        _draw_x_eye(surface, mx + eye_offset_x, my - eye_offset_y, eye_r)
    else:
        for ex in (mx - eye_offset_x, mx + eye_offset_x):
            ey = my - eye_offset_y
            pygame.draw.circle(surface, (255, 255, 255), (ex, ey), eye_r)
            pygame.draw.circle(surface, (30, 20, 10), (ex + 1, ey + 1), max(2, eye_r - 1))
            pygame.draw.circle(surface, (255, 255, 255), (ex + 1, ey - 1), max(1, eye_r // 3))

    nose_rect = (mx - radius // 5, my + radius // 6, radius * 2 // 5, radius // 5)
    pygame.draw.ellipse(surface, COLORS["mole_nose"], nose_rect)

    mouth_rect = pygame.Rect(mx - radius // 3, my + radius // 4, radius * 2 // 3, radius // 3)
    if whacked:
        pygame.draw.arc(surface, (30, 20, 10), mouth_rect, math.pi, 2 * math.pi, 2)
    else:
        pygame.draw.arc(surface, (30, 20, 10), mouth_rect, math.pi, 2 * math.pi, 2)


def _draw_x_eye(surface: pygame.Surface, ex: int, ey: int, r: int) -> None:
    pygame.draw.line(surface, (30, 20, 10), (ex - r, ey - r), (ex + r, ey + r), 2)
    pygame.draw.line(surface, (30, 20, 10), (ex + r, ey - r), (ex - r, ey + r), 2)


def _draw_whack_rays(surface: pygame.Surface, cx: int, cy: int, radius: int) -> None:
    ray_count = 8
    ray_len = radius * 2
    for i in range(ray_count):
        angle = (2 * math.pi / ray_count) * i
        x2 = int(cx + math.cos(angle) * ray_len)
        y2 = int(cy + math.sin(angle) * ray_len)
        pygame.draw.line(surface, COLORS["whacked"], (cx, cy), (x2, y2), 3)


def _draw_cell(
    surface: pygame.Surface,
    cx: int, cy: int,
    cell_size: int,
    mole,
) -> None:
    hole_rx = int(cell_size * 0.30)
    hole_ry = int(cell_size * 0.18)
    radius = int(cell_size * 0.22)

    _draw_hole(surface, cx, cy, hole_rx, hole_ry)

    if mole.state == MoleState.HIDDEN:
        return

    progress = mole.progress
    hidden_cy = cy + hole_ry + radius
    visible_cy = cy - hole_ry - int(radius * 0.3)
    mole_cy = int(hidden_cy + (visible_cy - hidden_cy) * progress)

    clip_rect = pygame.Rect(cx - hole_rx, 0, hole_rx * 2, cy + hole_ry)
    old_clip = surface.get_clip()
    surface.set_clip(clip_rect)

    whacked = mole.state == MoleState.WHACKED
    _draw_mole_head(surface, cx, mole_cy, radius, whacked, mole.whack_flash)

    if whacked and mole.whack_flash > 0:
        _draw_whack_rays(surface, cx, mole_cy, radius)

    surface.set_clip(old_clip)


def draw_grid(surface: pygame.Surface, state) -> None:
    cell_size, ox, oy = compute_layout(state.config)
    for row in range(state.config.grid_rows):
        for col in range(state.config.grid_cols):
            cx = ox + col * cell_size + cell_size // 2
            cy = oy + row * cell_size + cell_size // 2
            mole = state.board.get(row, col)
            _draw_cell(surface, cx, cy, cell_size, mole)


def draw_hud(
    surface: pygame.Surface,
    state,
    font_large: pygame.font.Font,
    font_medium: pygame.font.Font,
) -> None:
    hud_rect = pygame.Rect(0, 0, WINDOW_W, HUD_H)
    pygame.draw.rect(surface, COLORS["hud_bg"], hud_rect)
    pygame.draw.line(surface, COLORS["hud_line"], (0, HUD_H - 2), (WINDOW_W, HUD_H - 2), 2)

    score_surf = font_large.render(f"Score: {state.score}", True, COLORS["text_gold"])
    surface.blit(score_surf, (20, 15))

    ratio = state.time_remaining / state.config.game_duration
    if ratio > 0.5:
        timer_color = COLORS["timer_ok"]
    elif ratio > 0.25:
        timer_color = COLORS["timer_warn"]
    else:
        timer_color = COLORS["timer_low"]

    secs = math.ceil(state.time_remaining)
    timer_surf = font_large.render(f"Time: {secs}s", True, timer_color)
    surface.blit(timer_surf, (WINDOW_W - timer_surf.get_width() - 20, 15))

    diff_color = DIFFICULTY_COLORS[state.config.difficulty]
    diff_label = state.config.difficulty.value.upper()
    diff_surf = font_medium.render(diff_label, True, diff_color)
    surface.blit(diff_surf, (WINDOW_W // 2 - diff_surf.get_width() // 2, 15))

    bar_x, bar_y = 20, HUD_H - 22
    bar_w = WINDOW_W - 40
    bar_h = 12
    pygame.draw.rect(surface, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
    fill_w = int(bar_w * max(0.0, ratio))
    if fill_w > 0:
        pygame.draw.rect(surface, timer_color, (bar_x, bar_y, fill_w, bar_h), border_radius=6)


def _draw_button(
    surface: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    font: pygame.font.Font,
    mouse_pos: Tuple[int, int],
    small: bool = False,
) -> None:
    hovered = rect.collidepoint(mouse_pos)
    color = COLORS["btn_hover"] if hovered else COLORS["btn_normal"]
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, COLORS["btn_border"], rect, 2, border_radius=8)
    text_surf = font.render(label, True, COLORS["btn_text"])
    tx = rect.centerx - text_surf.get_width() // 2
    ty = rect.centery - text_surf.get_height() // 2
    surface.blit(text_surf, (tx, ty))


def draw_menu(
    surface: pygame.Surface,
    state,
    font_title: pygame.font.Font,
    font_large: pygame.font.Font,
    font_medium: pygame.font.Font,
    mouse_pos: Tuple[int, int],
) -> Dict[str, pygame.Rect]:
    cx = WINDOW_W // 2

    shadow = font_title.render("WHACK-A-MOLE", True, (10, 30, 10))
    title = font_title.render("WHACK-A-MOLE", True, COLORS["text_gold"])
    surface.blit(shadow, (cx - shadow.get_width() // 2 + 3, 83))
    surface.blit(title, (cx - title.get_width() // 2, 80))

    btn_w, btn_h = 50, 40
    row_y = 230

    label_size = font_large.render(
        f"{state.config.grid_size}×{state.config.grid_size}", True, COLORS["text_white"]
    )
    surface.blit(label_size, (cx - label_size.get_width() // 2, row_y + 5))

    caption = font_medium.render("Grid Size", True, COLORS["text_gold"])
    surface.blit(caption, (cx - caption.get_width() // 2, row_y - 28))

    prev_size_rect = pygame.Rect(cx - 120 - btn_w, row_y, btn_w, btn_h)
    next_size_rect = pygame.Rect(cx + 120, row_y, btn_w, btn_h)
    _draw_button(surface, prev_size_rect, "<", font_large, mouse_pos)
    _draw_button(surface, next_size_rect, ">", font_large, mouse_pos)

    row_y2 = 340
    caption2 = font_medium.render("Duration", True, COLORS["text_gold"])
    surface.blit(caption2, (cx - caption2.get_width() // 2, row_y2 - 28))

    label_dur = font_large.render(f"{state.config.game_duration}s", True, COLORS["text_white"])
    surface.blit(label_dur, (cx - label_dur.get_width() // 2, row_y2 + 5))

    prev_dur_rect = pygame.Rect(cx - 120 - btn_w, row_y2, btn_w, btn_h)
    next_dur_rect = pygame.Rect(cx + 120, row_y2, btn_w, btn_h)
    _draw_button(surface, prev_dur_rect, "<", font_large, mouse_pos)
    _draw_button(surface, next_dur_rect, ">", font_large, mouse_pos)

    row_y3 = 450
    caption3 = font_medium.render("Difficulty", True, COLORS["text_gold"])
    surface.blit(caption3, (cx - caption3.get_width() // 2, row_y3 - 28))

    diff_color = DIFFICULTY_COLORS[state.config.difficulty]
    diff_name = state.config.difficulty.value.upper()
    label_diff = font_large.render(diff_name, True, diff_color)
    surface.blit(label_diff, (cx - label_diff.get_width() // 2, row_y3 + 5))

    prev_diff_rect = pygame.Rect(cx - 120 - btn_w, row_y3, btn_w, btn_h)
    next_diff_rect = pygame.Rect(cx + 120, row_y3, btn_w, btn_h)
    _draw_button(surface, prev_diff_rect, "<", font_large, mouse_pos)
    _draw_button(surface, next_diff_rect, ">", font_large, mouse_pos)

    play_rect = pygame.Rect(cx - 100, 545, 200, 55)
    _draw_button(surface, play_rect, "PLAY", font_large, mouse_pos)

    hint = font_medium.render("Click a mole to whack it!", True, COLORS["text_white"])
    surface.blit(hint, (cx - hint.get_width() // 2, 620))

    return {
        "prev_size": prev_size_rect,
        "next_size": next_size_rect,
        "prev_dur": prev_dur_rect,
        "next_dur": next_dur_rect,
        "prev_diff": prev_diff_rect,
        "next_diff": next_diff_rect,
        "play": play_rect,
    }


def draw_gameover(
    surface: pygame.Surface,
    state,
    high_score: int,
    font_title: pygame.font.Font,
    font_large: pygame.font.Font,
    font_medium: pygame.font.Font,
    mouse_pos: Tuple[int, int],
) -> Dict[str, pygame.Rect]:
    overlay = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    cx = WINDOW_W // 2

    shadow = font_title.render("GAME OVER", True, (10, 10, 10))
    title = font_title.render("GAME OVER", True, COLORS["text_gold"])
    surface.blit(shadow, (cx - shadow.get_width() // 2 + 3, 153))
    surface.blit(title, (cx - title.get_width() // 2, 150))

    score_surf = font_large.render(f"Score: {state.score}", True, COLORS["text_white"])
    surface.blit(score_surf, (cx - score_surf.get_width() // 2, 240))

    hs_surf = font_large.render(f"Best: {high_score}", True, COLORS["text_gold"])
    surface.blit(hs_surf, (cx - hs_surf.get_width() // 2, 285))

    play_again_rect = pygame.Rect(cx - 210, 360, 190, 52)
    menu_rect = pygame.Rect(cx + 20, 360, 190, 52)
    _draw_button(surface, play_again_rect, "PLAY AGAIN", font_large, mouse_pos)
    _draw_button(surface, menu_rect, "MENU", font_large, mouse_pos)

    return {"play_again": play_again_rect, "menu": menu_rect}
