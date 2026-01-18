from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

from minimal_pong.entity import Entity

if TYPE_CHECKING:
    from minimal_pong.game import Game


class PaddleDirection(Enum):
    UP = auto()
    DOWN = auto()
    NONE = auto()


class Paddle(Entity):
    def __init__(
        self,
        game: Game,
        pos_x: float | int,
        pos_y: float | int,
        width: float | int,
        height: float | int,
        speed: float | int,
    ) -> None:
        self.game = game
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed

        self.rect = pygame.Rect(
            self.pos_x,
            0,
            self.width,
            self.height,
        )
        self.rect.centery = self.pos_y
        self.direction = PaddleDirection.NONE

    @property
    def at_top(self) -> bool:
        return self.rect.top <= 0

    @property
    def at_bottom(self) -> bool:
        return self.rect.bottom >= self.game.screen_height

    def update(self, dt: float) -> None:
        if self.direction is PaddleDirection.UP and not self.at_top:
            self.rect.centery -= self.speed * dt

        elif self.direction is PaddleDirection.DOWN and not self.at_bottom:
            self.rect.centery += self.speed * dt

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, pygame.Color('white'), self.rect)
