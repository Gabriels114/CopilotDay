from dataclasses import dataclass
from enum import Enum

from config import GameConfig
from board import Board


class Phase(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAMEOVER = "gameover"


@dataclass(frozen=True)
class GameState:
    phase: Phase
    config: GameConfig
    board: Board
    score: int
    time_remaining: float
    spawn_timer: float

    @classmethod
    def menu(cls, config: GameConfig) -> "GameState":
        board = Board.create(config.grid_rows, config.grid_cols)
        return cls(
            phase=Phase.MENU,
            config=config,
            board=board,
            score=0,
            time_remaining=float(config.game_duration),
            spawn_timer=0.0,
        )

    def start(self) -> "GameState":
        board = Board.create(self.config.grid_rows, self.config.grid_cols)
        return GameState(
            phase=Phase.PLAYING,
            config=self.config,
            board=board,
            score=0,
            time_remaining=float(self.config.game_duration),
            spawn_timer=0.0,
        )

    def update(self, dt: float) -> "GameState":
        if self.phase != Phase.PLAYING:
            return self
        new_time = self.time_remaining - dt
        if new_time <= 0.0:
            return GameState(
                phase=Phase.GAMEOVER,
                config=self.config,
                board=self.board,
                score=self.score,
                time_remaining=0.0,
                spawn_timer=self.spawn_timer,
            )

        new_board = self.board.update(dt, self.config.mole_visible_time)
        new_spawn_timer = self.spawn_timer + dt

        if new_spawn_timer >= self.config.mole_spawn_interval:
            new_board = new_board.try_spawn()
            new_spawn_timer = 0.0

        return GameState(
            phase=Phase.PLAYING,
            config=self.config,
            board=new_board,
            score=self.score,
            time_remaining=new_time,
            spawn_timer=new_spawn_timer,
        )

    def whack(self, row: int, col: int) -> "GameState":
        new_board, hit = self.board.try_whack(row, col)
        new_score = self.score + (1 if hit else 0)
        return GameState(
            phase=self.phase,
            config=self.config,
            board=new_board,
            score=new_score,
            time_remaining=self.time_remaining,
            spawn_timer=self.spawn_timer,
        )

    def with_config(self, config: GameConfig) -> "GameState":
        board = Board.create(config.grid_rows, config.grid_cols)
        return GameState(
            phase=self.phase,
            config=config,
            board=board,
            score=self.score,
            time_remaining=float(config.game_duration),
            spawn_timer=self.spawn_timer,
        )
