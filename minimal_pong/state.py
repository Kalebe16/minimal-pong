from abc import ABC, abstractmethod

import pygame


class State(ABC):
    @abstractmethod
    def on_enter(self) -> None:
        pass

    @abstractmethod
    def on_exit(self) -> None:
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        pass
