from __future__ import annotations

import random
from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

from minimal_pong.audios import TUC_AUDIO
from minimal_pong.entities.paddle import Paddle
from minimal_pong.entity import Entity

if TYPE_CHECKING:
    from minimal_pong.game import Game


class BallDirection(Enum):
    LEFT_UP = auto()
    LEFT_DOWN = auto()
    RIGHT_UP = auto()
    RIGHT_DOWN = auto()


class Ball(Entity):
    def __init__(
        self,
        game: Game,
        left_paddle: Paddle,
        right_paddle: Paddle,
        width: float | int,
        height: float | int,
        speed: float | int,
        border_radius: float | int,
    ) -> None:
        self.game = game
        self.left_paddle = left_paddle
        self.right_paddle = right_paddle
        self.width = width
        self.height = height
        self.speed = speed
        self.border_radius = border_radius

        self.tuc_audio = pygame.mixer.Sound(str(TUC_AUDIO))
        self.rect = pygame.Rect(
            0,
            0,
            self.width,
            self.height,
        )
        self.rect.centerx = self.game.screen_width // 2
        self.rect.centery = self.game.screen_height // 2
        self.direction = random.choice(
            [
                BallDirection.RIGHT_DOWN,
                BallDirection.RIGHT_UP,
                BallDirection.LEFT_DOWN,
                BallDirection.LEFT_UP,
            ]
        )

    @property
    def at_top(self) -> bool:
        return self.rect.top <= 0

    @property
    def at_bottom(self) -> bool:
        return self.rect.bottom >= self.game.screen_height

    @property
    def exited_left(self) -> bool:
        return self.rect.right < 0

    @property
    def exited_right(self) -> bool:
        return self.rect.left > self.game.screen_width

    @property
    def at_left_paddle(self) -> bool:
        return self.rect.colliderect(self.left_paddle.rect)

    @property
    def at_right_paddle(self) -> bool:
        return self.rect.colliderect(self.right_paddle.rect)

    def reset_pos(self) -> None:
        self.rect.centerx = self.game.screen_width // 2
        self.rect.centery = self.game.screen_height // 2

    def update(self, dt: float) -> None:
        if self.direction == BallDirection.RIGHT_DOWN:
            self.rect.centerx += self.speed * dt
            self.rect.centery += self.speed * dt
        elif self.direction == BallDirection.RIGHT_UP:
            self.rect.centerx += self.speed * dt
            self.rect.centery -= self.speed * dt
        elif self.direction == BallDirection.LEFT_DOWN:
            self.rect.centerx -= self.speed * dt
            self.rect.centery += self.speed * dt
        elif self.direction == BallDirection.LEFT_UP:
            self.rect.centerx -= self.speed * dt
            self.rect.centery -= self.speed * dt

        if self.at_top:
            if self.direction == BallDirection.RIGHT_UP:
                self.direction = BallDirection.RIGHT_DOWN
            elif self.direction == BallDirection.LEFT_UP:
                self.direction = BallDirection.LEFT_DOWN
            self.tuc_audio.stop()
            self.tuc_audio.play()
        elif self.at_bottom:
            if self.direction == BallDirection.RIGHT_DOWN:
                self.direction = BallDirection.RIGHT_UP
            elif self.direction == BallDirection.LEFT_DOWN:
                self.direction = BallDirection.LEFT_UP
            self.tuc_audio.stop()
            self.tuc_audio.play()
        elif self.at_left_paddle:
            if self.direction == BallDirection.LEFT_UP:
                self.direction = BallDirection.RIGHT_UP
            elif self.direction == BallDirection.LEFT_DOWN:
                self.direction = BallDirection.RIGHT_DOWN
            self.tuc_audio.stop()
            self.tuc_audio.play()
        elif self.at_right_paddle:
            if self.direction == BallDirection.RIGHT_UP:
                self.direction = BallDirection.LEFT_UP
            elif self.direction == BallDirection.RIGHT_DOWN:
                self.direction = BallDirection.LEFT_DOWN
            self.tuc_audio.stop()
            self.tuc_audio.play()

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            pygame.Color('white'),
            self.rect,
            border_radius=self.border_radius,
        )
