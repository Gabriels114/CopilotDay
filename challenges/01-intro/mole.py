from dataclasses import dataclass
from enum import Enum


class MoleState(Enum):
    HIDDEN = "hidden"
    RISING = "rising"
    VISIBLE = "visible"
    FALLING = "falling"
    WHACKED = "whacked"


RISE_SPEED = 2.5
FALL_SPEED = 3.0
WHACK_FLASH_DURATION = 0.5


@dataclass(frozen=True)
class Mole:
    state: MoleState = MoleState.HIDDEN
    progress: float = 0.0
    time_visible: float = 0.0
    whack_flash: float = 0.0

    def update(self, dt: float, visible_duration: float) -> "Mole":
        if self.state == MoleState.RISING:
            new_progress = min(1.0, self.progress + RISE_SPEED * dt)
            if new_progress >= 1.0:
                return Mole(MoleState.VISIBLE, 1.0, 0.0, self.whack_flash)
            return Mole(
                MoleState.RISING, new_progress, self.time_visible, self.whack_flash
            )

        if self.state == MoleState.VISIBLE:
            new_time = self.time_visible + dt
            if new_time >= visible_duration:
                return Mole(MoleState.FALLING, 1.0, new_time, self.whack_flash)
            return Mole(MoleState.VISIBLE, 1.0, new_time, self.whack_flash)

        if self.state == MoleState.FALLING:
            new_progress = max(0.0, self.progress - FALL_SPEED * dt)
            if new_progress <= 0.0:
                return Mole(MoleState.HIDDEN, 0.0, 0.0, 0.0)
            return Mole(
                MoleState.FALLING, new_progress, self.time_visible, self.whack_flash
            )

        if self.state == MoleState.WHACKED:
            new_flash = max(0.0, self.whack_flash - dt)
            new_progress = max(0.0, self.progress - FALL_SPEED * dt)
            if new_progress <= 0.0:
                return Mole(MoleState.HIDDEN, 0.0, 0.0, 0.0)
            return Mole(MoleState.WHACKED, new_progress, self.time_visible, new_flash)

        return self

    def spawn(self) -> "Mole":
        return Mole(MoleState.RISING, 0.0, 0.0, 0.0)

    def whack(self) -> "Mole":
        if self.state in (MoleState.RISING, MoleState.VISIBLE):
            return Mole(
                MoleState.WHACKED,
                self.progress,
                self.time_visible,
                WHACK_FLASH_DURATION,
            )
        return self

    def is_whackable(self) -> bool:
        return self.state in (MoleState.RISING, MoleState.VISIBLE)
