"""RGB color picker tool."""

import pygame
from pygame_widgets.slider import Slider as PygameSlider
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
            self.x, self.y, self.width, self.height, (0, 0, 0), "Red", self.window
        )
        self.green = Slider(
            self.x,
            self.y + self.height + 45,
            self.width,
            self.height,
            (0, 0, 0),
            "Green",
            self.window,
        )
        self.blue = Slider(
            self.x,
            self.y + (self.height * 2) + 90,
            self.width,
            self.height,
            (0, 0, 0),
            "Blue",
            self.window,
        )
        self.alpha = Slider(
            self.x,
            self.y + (self.height * 3) + 135,
            self.width,
            self.height,
            (0, 0, 0),
            "Alpha",
            self.window,
        )
        self.alpha.slider.setValue(255)
        self.color_rect = pygame.Rect(
            self.x + 25, self.y + (self.height * 3) + 180, 50, 50
        )

    @property
    def rect_color(self) -> pygame.Color:
        """Return the color based on the sliders."""
        return self._rect_color

    @rect_color.setter
    def rect_color(self, value: tuple[int, int, int, int]) -> None:
        """Set the color with value."""
        r, g, b, a = value
        self._rect_color.r = r
        self._rect_color.g = g
        self._rect_color.b = b
        self._rect_color.a = a

    def render(self, window: pygame.Surface) -> None:
        """Render each slider and their texts."""
        self.red.render(window)
        self.green.render(window)
        self.blue.render(window)
        self.alpha.render(window)

        pygame.draw.rect(window, self._rect_color, self.color_rect)
        pygame.draw.rect(window, (0, 0, 0), self.color_rect, width=1)

    def update(self) -> None:
        """Update the color basen on the values of the slider."""
        self.red.update()
        self.green.update()
        self.blue.update()
        self.alpha.update()

        self.rect_color = (
            self.red.get_value(),
            self.green.get_value(),
            self.blue.get_value(),
            self.alpha.get_value(),
        )


class Slider(Object):
    """Creating a better Slider with textbox and titles included."""

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: tuple,
        title: str,
        window: pygame.Surface,
    ):
        super().__init__(x, y, width, height, color)
        self.title = title
        self.window = window

        self.slider = PygameSlider(
            self.window, self.x, self.y, self.width, self.height, min=0, max=255, step=1
        )
        self.slider_input = TextBox(
            self.window, self.x + self.width + 20, self.y - 20, 45, 45
        )
        self.slider_input.onTextChanged = self.text_changed
        self.slider_input.setText("127")

        self.font = pygame.font.SysFont("Arial", 20)

    def text_changed(self) -> None:
        """This method is called, when the input is written."""
        slider_value = self.slider_input.getText()
        if self.is_int(slider_value):
            self.slider.setValue(int(slider_value))
        else:
            self.slider.setValue(0)

    def is_int(self, value: any) -> bool:
        """This function checks if the given value could be an int."""
        try:
            int(value)
            return True
        except ValueError:
            return False

    def update(self) -> None:
        """Update the color basen on the values of the slider."""
        self.slider_input.setText(str(self.slider.value))

    def render(self, _) -> None:
        """Render each slider and their texts."""
        text_surface = self.font.render(self.title, False, (0, 0, 0))
        x_offset = (self.width / 2) - text_surface.get_size()[0] / 2
        self.window.blit(text_surface, (self.x + x_offset, self.slider.getY() - 25))
        self.slider.draw()
        self.slider_input.draw()

    def get_value(self) -> int:
        """Returns the slider value"""
        return self.slider.value
