"""This module defines the program itself."""

import pygame
import pygame_widgets

from tile import Tile
from tools.colorpicker import ColorPicker
from tools.object import Object


class Program:
    """
    This class runs the PixelEditor program.

    Attributes
    ----------
    width : int
        The width of the program window.
    height : int
        The height of the program window.
    title : str
        The title of the program window.
    sprite_size : int
        The size of the sprite (sprite_size x sprite_size).
    """

    def __init__(self, width: int, height: int, title: str, sprite_size: int) -> None:
        self._window_width = width
        self._window_height = height
        self.title = title
        self.sprite_size = sprite_size

        self.window = pygame.display.set_mode((self._window_width, self._window_height))
        pygame.display.set_caption(self.title)

        self.surface = pygame.Surface(
            (self._window_width, self._window_height),
            pygame.SRCALPHA,  # pylint: disable=no-member
        )

        self._canvas_width = 1024  # Later make it scaleable
        self._canvas_height = 768

        self.background_color = (127, 127, 127, 0)

        self.objects: list[Object] = []
        self.is_running = False

        self.setup_tools()

    @property
    def window_width(self) -> int:
        """This method returns the canvas width."""
        return self._window_width

    @property
    def window_height(self) -> int:
        """This method returns the canvas width."""
        return self._window_height

    def setup_tools(self) -> None:
        """This method will create every tool for the editor."""
        pygame.font.init()

        self.color_picker = ColorPicker(20, 70, 100, 20, (0, 0, 0), self.window)

    def start(self):
        """This method sets the tools up and starts the program."""
        self.is_running = True

        self.objects.append(self.color_picker)

        self.create_borders()

        self.loop()

    def loop(self) -> None:
        """Main loop of the pixel editor."""
        while self.is_running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    self.is_running = False

            self.update(events)
            self.render()

        pygame.quit()  # pylint: disable=no-member

    def update(self, events: list[pygame.event.Event]) -> None:
        """This method updates every object inside the program."""
        for o in self.objects:
            o.update()
        pygame_widgets.update(events)

    def render(self) -> None:
        """This method renders every object inside the program."""
        self.window.fill((127, 127, 127))

        for o in self.objects:
            o.render(self.surface)

        self.window.blit(self.surface, (0, 0))

        pygame.display.flip()

    def create_borders(self) -> None:
        """This function draws a tile map on the given window."""
        x_offset = (self._window_width - self._canvas_width) / 2
        y_offset = (self._window_height - self._canvas_height) / 2

        for i in range(self.sprite_size):
            for j in range(self.sprite_size):
                tile_width = self._canvas_width / self.sprite_size
                tile_height = self._canvas_height / self.sprite_size
                t = Tile(
                    x_offset + (i * tile_width),
                    y_offset + (j * tile_height),
                    tile_width,
                    tile_height,
                    self.background_color,
                )
                t.get_color.return_value = self.color_picker.rect_color
                t.get_window_width.return_value = self.window_width
                t.get_window_height.return_value = self.window_height
                self.objects.append(t)
