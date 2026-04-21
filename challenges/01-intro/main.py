import pygame

from config import GameConfig
from game import GameState, Phase
from renderer import (
    WINDOW_W, WINDOW_H, FPS,
    compute_layout, pixel_to_cell,
    draw_background, draw_grid, draw_hud,
    draw_menu, draw_gameover,
)

_FONT_CANDIDATES = ["Arial", "Helvetica", "DejaVu Sans", "FreeSans", ""]


def _load_font(size: int, bold: bool = False) -> pygame.font.Font:
    for name in _FONT_CANDIDATES:
        try:
            font = pygame.font.SysFont(name, size, bold=bold)
            return font
        except pygame.error:
            continue
    return pygame.font.Font(None, size)


def _handle_menu_click(
    state: GameState,
    pos: tuple,
    button_rects: dict,
) -> GameState:
    if "prev_size" in button_rects and button_rects["prev_size"].collidepoint(pos):
        return state.with_config(state.config.prev_size())
    if "next_size" in button_rects and button_rects["next_size"].collidepoint(pos):
        return state.with_config(state.config.next_size())
    if "prev_dur" in button_rects and button_rects["prev_dur"].collidepoint(pos):
        return state.with_config(state.config.prev_duration())
    if "next_dur" in button_rects and button_rects["next_dur"].collidepoint(pos):
        return state.with_config(state.config.next_duration())
    if "prev_diff" in button_rects and button_rects["prev_diff"].collidepoint(pos):
        return state.with_config(state.config.prev_difficulty())
    if "next_diff" in button_rects and button_rects["next_diff"].collidepoint(pos):
        return state.with_config(state.config.next_difficulty())
    if "play" in button_rects and button_rects["play"].collidepoint(pos):
        return state.start()
    return state


def _handle_gameover_click(
    state: GameState,
    pos: tuple,
    button_rects: dict,
) -> GameState:
    if "play_again" in button_rects and button_rects["play_again"].collidepoint(pos):
        return state.start()
    if "menu" in button_rects and button_rects["menu"].collidepoint(pos):
        return GameState.menu(state.config)
    return state


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Whack-a-Mole")
    clock = pygame.time.Clock()

    font_title = _load_font(72, bold=True)
    font_large = _load_font(36, bold=True)
    font_medium = _load_font(26)

    state = GameState.menu(GameConfig())
    high_score = 0
    button_rects: dict = {}

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state.phase == Phase.MENU:
                    state = _handle_menu_click(state, event.pos, button_rects)

                elif state.phase == Phase.PLAYING:
                    cell_size, ox, oy = compute_layout(state.config)
                    cell = pixel_to_cell(event.pos[0], event.pos[1], state.config, cell_size, ox, oy)
                    if cell is not None:
                        state = state.whack(cell[0], cell[1])

                elif state.phase == Phase.GAMEOVER:
                    state = _handle_gameover_click(state, event.pos, button_rects)

        if state.phase == Phase.PLAYING:
            state = state.update(dt)
            if state.phase == Phase.GAMEOVER:
                high_score = max(high_score, state.score)

        draw_background(screen)

        if state.phase == Phase.MENU:
            button_rects = draw_menu(screen, state, font_title, font_large, font_medium, mouse_pos)
        elif state.phase == Phase.PLAYING:
            draw_grid(screen, state)
            draw_hud(screen, state, font_large, font_medium)
        elif state.phase == Phase.GAMEOVER:
            draw_grid(screen, state)
            draw_hud(screen, state, font_large, font_medium)
            button_rects = draw_gameover(screen, state, high_score, font_title, font_large, font_medium, mouse_pos)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
