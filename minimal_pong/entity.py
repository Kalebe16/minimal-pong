from abc import ABC, abstractmethod

import pygame


class Entity(ABC):
    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None: ...
