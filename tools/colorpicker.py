"""RGB color picker tool."""

import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from tools.object import Object


class ColorPicker(Object):
    """
    This class creates a hsl type color picker.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: tuple,
        window: pygame.Surface,
    ):
        super().__init__(x, y, width, height, color)
        self.window = window
        self.font = pygame.font.SysFont("Arial", 20)

        self._rect_color = pygame.Color(0)

        self.red = Slider(
            self.window, self.x, self.y, self.width, self.height, min=0, max=255, step=1
        )
        self.red_input = TextBox(
            self.window, self.x + self.width + 20, self.y - 20, 45, 45
        )
        self.red_input.onTextChanged = self.text_changed
        self.red_input.setText("127")
        self.green = Slider(
            self.window,
            self.x,
            self.y + self.height + 45,
            self.width,
            self.height,
            min=0,
            max=255,
            step=1,
        )
        self.green_input = TextBox(
            self.window, self.x + self.width + 20, self.y + self.height + 25, 45, 45
        )
        self.green_input.onTextChanged = self.text_changed
        self.green_input.setText("127")
        self.blue = Slider(
            self.window,
            self.x,
            self.y + (self.height * 2) + 90,
            self.width,
            self.height,
            min=0,
            max=255,
            step=1,
        )
        self.blue_input = TextBox(
            self.window,
            self.x + self.width + 20,
            self.y + (self.height * 2) + 70,
            45,
            45,
        )
        self.blue_input.onTextChanged = self.text_changed
        self.blue_input.setText("127")
        self.color_rect = pygame.Rect(
            self.x + 25, self.y + (self.height * 2) + 135, 50, 50
        )

    @property
    def rect_color(self) -> pygame.Color:
        """Return the color based on the sliders."""
        return self._rect_color

    @rect_color.setter
    def rect_color(self, value: tuple[int, int, int]) -> None:
        """Set the color with value."""
        r, g, b = value
        self._rect_color.r = r
        self._rect_color.g = g
        self._rect_color.b = b

    def render(self, window: pygame.Surface) -> None:
        """Render each slider and their texts."""
        text_surface = self.font.render("Red", False, (0, 0, 0))
        x_offset = (self.width / 2) - text_surface.get_size()[0] / 2
        window.blit(text_surface, (self.x + x_offset, self.red.getY() - 25))
        self.red.draw()

        text_surface = self.font.render("Green", False, (0, 0, 0))
        x_offset = (self.width / 2) - text_surface.get_size()[0] / 2
        window.blit(text_surface, (self.x + x_offset, self.green.getY() - 25))
        self.green.draw()

        text_surface = self.font.render("Blue", False, (0, 0, 0))
        x_offset = (self.width / 2) - text_surface.get_size()[0] / 2
        window.blit(text_surface, (self.x + x_offset, self.blue.getY() - 25))
        self.blue.draw()

        pygame.draw.rect(window, self._rect_color, self.color_rect)
        pygame.draw.rect(window, (0, 0, 0), self.color_rect, width=1)

        self.red_input.draw()
        self.green_input.draw()
        self.blue_input.draw()

    def update(self) -> None:
        """Update the color basen on the values of the slider."""
        self.rect_color = (
            self.red.getValue(),
            self.green.getValue(),
            self.blue.getValue(),
        )
        self.red_input.setText(str(self.red.value))
        self.green_input.setText(str(self.green.value))
        self.blue_input.setText(str(self.blue.value))

    def text_changed(self) -> None:
        """This method is called, when any input is written."""
        red_value = self.red_input.getText()
        if self.is_int(red_value):
            self.red.setValue(int(red_value))
        else:
            self.red.setValue(0)
        green_value = self.green_input.getText()
        if self.is_int(green_value):
            self.green.setValue(int(green_value))
        else:
            self.green.setValue(0)
        blue_value = self.blue_input.getText()
        if self.is_int(blue_value):
            self.blue.setValue(int(blue_value))
        else:
            self.blue.setValue(0)

    def is_int(self, value: any) -> bool:
        """This function checks if the given value could be an int."""
        try:
            int(value)
            return True
        except ValueError:
            return False
