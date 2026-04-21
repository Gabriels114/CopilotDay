import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import pygame


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture()
def screen_surface():
    return pygame.Surface((800, 700), pygame.SRCALPHA)


@pytest.fixture()
def font_small():
    return pygame.font.Font(None, 24)


@pytest.fixture()
def font_large():
    return pygame.font.Font(None, 36)
