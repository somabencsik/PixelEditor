"""This module handles every object inside the program."""

import pygame


class Object:
    """
    An Object inside the program.

    Attributes
    ----------
    x : float
        X position of object on the window.
    y : float
        Y position of object on the window.
    width : float
        Width of the object.
    height : float
        Height of the object.
    color : tuple
        Color or the object
    """

    def __init__(self, x: float, y: float, width: float, height: float, color: tuple):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect(x, y, width, height)

    def on_click(self) -> None:
        """Callback when the object is being clicked."""

    def update(self) -> None:
        """This method will be called in every frame."""
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                self.x < mouse_x < self.x + self.width
                and self.y < mouse_y < self.y + self.height
            ):
                self.on_click()

    def render(self, window: pygame.Surface) -> None:
        """This method will draw the current object's rect."""
        pygame.draw.rect(window, self.color, self.rect, width=0)
        pygame.draw.rect(window, (0, 0, 0), self.rect, width=1)
