from __future__ import annotations

import random
from typing import TYPE_CHECKING, Literal

import pygame

from minimal_pong.audios import SCORE_AUDIO, VICTORY_AUDIO
from minimal_pong.entities.ball import Ball, BallDirection
from minimal_pong.entities.paddle import Paddle, PaddleDirection
from minimal_pong.state import State

if TYPE_CHECKING:
    from minimal_pong.game import Game


class PlayState(State):
    WINNER_TEXT = """
        {winner} WINS!\n\
(Press 'R' to play again)\
"""
    PAUSED_TEXT = """
         PAUSED\n\
(Press 'Q' to go menu)\n\
(Press 'ESCAPE' to unpause)\
"""

    def __init__(self, game: Game) -> None:
        self.game = game
        self.font = pygame.font.SysFont(None, 64)
        self.score_audio = pygame.mixer.Sound(str(SCORE_AUDIO))
        self.victory_audio = pygame.mixer.Sound(str(VICTORY_AUDIO))

    def on_enter(self) -> None:
        self.left_paddle = Paddle(
            game=self.game,
            pos_x=0,
            pos_y=self.game.screen_height // 2,
            width=20,
            height=300,
            speed=300,
        )
        self.right_paddle = Paddle(
            game=self.game,
            pos_x=self.game.screen_width - 20,
            pos_y=self.game.screen_height // 2,
            width=20,
            height=300,
            speed=300,
        )
        self.ball = Ball(
            game=self.game,
            left_paddle=self.left_paddle,
            right_paddle=self.right_paddle,
            width=20,
            height=20,
            border_radius=10,
            speed=700,
        )
        self.left_score = 0
        self.right_score = 0
        self.round_delay = 1
        self.winner: Literal['RIGHT', 'LEFT'] | None = None
        self.paused = False

    def on_exit(self) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.left_paddle.direction = PaddleDirection.UP
        elif keys[pygame.K_s]:
            self.left_paddle.direction = PaddleDirection.DOWN
        else:
            self.left_paddle.direction = PaddleDirection.NONE

        if keys[pygame.K_UP]:
            self.right_paddle.direction = PaddleDirection.UP
        elif keys[pygame.K_DOWN]:
            self.right_paddle.direction = PaddleDirection.DOWN
        else:
            self.right_paddle.direction = PaddleDirection.NONE

        if keys[pygame.K_r] and self.winner:
            self.left_score = 0
            self.right_score = 0
            self.winner = None
            self.ball.reset_pos()
            self.round_delay = 1.0

        if keys[pygame.K_ESCAPE] and not self.winner:
            self.paused = not self.paused

        if keys[pygame.K_q] and self.paused:
            self.game.set_state(self.game.menu_state)

    def update(self, dt: float) -> None:
        if self.winner:
            return
        if self.paused:
            return

        self.left_paddle.update(dt)
        self.right_paddle.update(dt)

        if self.round_delay > 0:
            self.round_delay = max(0.0, self.round_delay - dt)
            return

        self.ball.update(dt)

        if self.ball.exited_left:
            self.right_score += 1
            self.ball.reset_pos()
            self.ball.direction = random.choice(
                [BallDirection.RIGHT_UP, BallDirection.RIGHT_DOWN]
            )
            self.round_delay = 1
            self.score_audio.play()

        elif self.ball.exited_right:
            self.left_score += 1
            self.ball.reset_pos()
            self.ball.direction = random.choice(
                [BallDirection.LEFT_UP, BallDirection.LEFT_DOWN]
            )
            self.round_delay = 1
            self.score_audio.play()

        if self.left_score >= 3:
            self.winner = 'LEFT'
            self.victory_audio.play()
        elif self.right_score >= 3:
            self.winner = 'RIGHT'
            self.victory_audio.play()

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(pygame.Color('black'))

        self.left_paddle.render(screen)
        self.right_paddle.render(screen)
        self.ball.render(screen)

        score = self.font.render(
            f'{self.left_score} - {self.right_score}',
            True,
            pygame.Color('white'),
        )
        score_rect = score.get_rect(center=(self.game.screen_width // 2, 200))
        screen.blit(score, score_rect)

        if self.winner:
            winner_text = self.font.render(
                self.WINNER_TEXT.format(winner=self.winner),
                True,
                pygame.Color('white'),
                1,
            )
            winner_rect = winner_text.get_rect(
                center=(
                    self.game.screen_width // 2,
                    self.game.screen_height // 2 + 100,
                )
            )
            screen.blit(winner_text, winner_rect)

        if self.paused:
            paused_text = self.font.render(
                self.PAUSED_TEXT, True, pygame.Color('white')
            )
            paused_rect = paused_text.get_rect(
                center=(
                    self.game.screen_width // 2,
                    self.game.screen_height // 2 + 100,
                )
            )
            screen.blit(paused_text, paused_rect)
