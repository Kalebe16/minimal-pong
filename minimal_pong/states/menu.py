from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

import pygame

from minimal_pong.state import State

if TYPE_CHECKING:
    from minimal_pong.game import Game


class MenuOption(Enum):
    START = auto()
    QUIT = auto()


class MenuState(State):
    def __init__(self, game: Game) -> None:
        self.game = game
        self.font = pygame.font.SysFont(None, 100)
        self.small_font = pygame.font.SysFont(None, 64)

    def on_enter(self) -> None:
        self.selected_option: MenuOption = MenuOption.START

    def on_exit(self) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_option = MenuOption.START

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_option = MenuOption.QUIT

            elif event.key == pygame.K_RETURN:
                if self.selected_option == MenuOption.START:
                    self.game.set_state(self.game.play_state)
                elif self.selected_option == MenuOption.QUIT:
                    self.game.stop()

    def update(self, dt: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(pygame.Color('black'))

        title = self.font.render('MINIMAL PONG', True, pygame.Color('white'))
        start = self.small_font.render('Start', True, pygame.Color('white'))
        quit = self.small_font.render('Quit', True, pygame.Color('white'))
        arrow = self.small_font.render('>', True, pygame.Color('white'))

        title_rect = title.get_rect(center=(self.game.screen_width // 2, 200))
        start_rect = start.get_rect(
            center=(self.game.screen_width // 2, self.game.screen_height // 2)
        )
        quit_rect = quit.get_rect(
            center=(
                self.game.screen_width // 2,
                self.game.screen_height // 2 + 60,
            )
        )

        if self.selected_option == MenuOption.START:
            arrow_rect = arrow.get_rect(
                midright=(start_rect.left - 10, start_rect.centery)
            )
        elif self.selected_option == MenuOption.QUIT:
            arrow_rect = arrow.get_rect(
                midright=(quit_rect.left - 10, quit_rect.centery)
            )

        screen.blit(title, title_rect)
        screen.blit(start, start_rect)
        screen.blit(quit, quit_rect)
        screen.blit(arrow, arrow_rect)
