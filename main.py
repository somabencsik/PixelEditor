"""
Created by: Soma Bencsik
Start date: 2024.05.02.
Using: Ubuntu 24.02
"""

from copy import deepcopy

import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


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


class Signal:
    """Signal to allow communication between objects."""

    return_value = None

    def emit(self) -> any:
        """Returns whatever is connected to it (If nothing, than None)."""
        return deepcopy(self.return_value)


class Tile(Object):
    """This class is to be able to fill the Object's color."""

    get_color = Signal()
    get_window_width = Signal()
    get_window_height = Signal()

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

        self._canvas_width = 1024  # Later make it scaleable
        self._canvas_height = 768

        self.background_color = (127, 127, 127)

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
            o.render(self.window)

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


if __name__ == "__main__":
    p = Program(1600, 900, "PixelEditor", 64)  # Later use settings
    p.start()
