import pygame

from minimal_pong.state import State
from minimal_pong.states.menu import MenuState
from minimal_pong.states.play import PlayState


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('Minimal Pong')

        self.play_state = PlayState(game=self)
        self.menu_state = MenuState(game=self)
        self.state: State | None = None
        self.set_state(self.menu_state)

        self.screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN,
            vsync=True,
            display=0,
        )
        self.screen_width, self.screen_height = self.screen.get_size()

        self.clock = pygame.time.Clock()
        self.running = True

    def set_state(self, state: State) -> None:
        if self.state:
            self.state.on_exit()
        self.state = state
        self.state.on_enter()

    def start(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1_000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

                self.state.handle_event(event)

            self.state.update(dt)
            self.state.render(self.screen)
            pygame.display.flip()

        pygame.quit()

    def stop(self) -> None:
        self.running = False
