from dataclasses import dataclass
from typing import Tuple

GRID_SIZES = [3, 4, 5]
DURATIONS = [15, 30, 45, 60, 90]

COLORS = {
    "bg_top":      (34,  100, 34),
    "bg_bottom":   (15,  60,  15),
    "hole_back":   (30,  18,  8),
    "hole_rim":    (60,  38,  18),
    "dirt":        (90,  55,  25),
    "mole_body":   (139, 90,  43),
    "mole_ear":    (110, 68,  28),
    "mole_shine":  (200, 160, 100),
    "mole_nose":   (220, 120, 140),
    "whacked":     (255, 215, 0),
    "hud_bg":      (20,  50,  20),
    "hud_line":    (60,  120, 60),
    "text_white":  (255, 255, 255),
    "text_gold":   (255, 215, 0),
    "text_dark":   (30,  20,  10),
    "btn_normal":  (60,  100, 60),
    "btn_hover":   (90,  140, 90),
    "btn_border":  (160, 200, 80),
    "btn_text":    (255, 255, 255),
    "timer_ok":    (80,  200, 80),
    "timer_warn":  (220, 180, 40),
    "timer_low":   (220, 60,  40),
}


@dataclass(frozen=True)
class GameConfig:
    grid_size: int = 3
    game_duration: int = 30
    mole_visible_time: float = 1.4
    mole_spawn_interval: float = 0.9

    @property
    def grid_rows(self) -> int:
        return self.grid_size

    @property
    def grid_cols(self) -> int:
        return self.grid_size

    def next_size(self) -> "GameConfig":
        idx = GRID_SIZES.index(self.grid_size)
        new_idx = (idx + 1) % len(GRID_SIZES)
        return GameConfig(
            grid_size=GRID_SIZES[new_idx],
            game_duration=self.game_duration,
            mole_visible_time=self.mole_visible_time,
            mole_spawn_interval=self.mole_spawn_interval,
        )

    def prev_size(self) -> "GameConfig":
        idx = GRID_SIZES.index(self.grid_size)
        new_idx = (idx - 1) % len(GRID_SIZES)
        return GameConfig(
            grid_size=GRID_SIZES[new_idx],
            game_duration=self.game_duration,
            mole_visible_time=self.mole_visible_time,
            mole_spawn_interval=self.mole_spawn_interval,
        )

    def next_duration(self) -> "GameConfig":
        idx = DURATIONS.index(self.game_duration)
        new_idx = (idx + 1) % len(DURATIONS)
        return GameConfig(
            grid_size=self.grid_size,
            game_duration=DURATIONS[new_idx],
            mole_visible_time=self.mole_visible_time,
            mole_spawn_interval=self.mole_spawn_interval,
        )

    def prev_duration(self) -> "GameConfig":
        idx = DURATIONS.index(self.game_duration)
        new_idx = (idx - 1) % len(DURATIONS)
        return GameConfig(
            grid_size=self.grid_size,
            game_duration=DURATIONS[new_idx],
            mole_visible_time=self.mole_visible_time,
            mole_spawn_interval=self.mole_spawn_interval,
        )
