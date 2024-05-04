"""This module defines a Tile."""

import pygame

from object_signal import ObjectSignal
from tools.object import Object


class Tile(Object):
    """This class is to be able to fill the Object's color."""

    get_color = ObjectSignal()
    get_window_width = ObjectSignal()
    get_window_height = ObjectSignal()

    def on_click(self) -> None:
        """When the tile is clicked, fill the object with the chosen color."""
        self.color = self.get_color.emit()

    def update(self) -> None:
        """This method changes the rect of the object to be scaled to the good ratio."""
        super().update()
        width_scaler = (self.width / self.get_window_width.emit()) * 100
        height_scaler = (self.height / self.get_window_height.emit()) * 100

        self.rect = pygame.Rect(
            self.x, self.y, self.width * width_scaler, self.height * height_scaler
        )
