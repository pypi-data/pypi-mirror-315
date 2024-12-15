from functools import partial
from typing import Callable

from hemline.colors import Color, default_colorize

from .alignment import Alignment, get_alignment_method
from .defaults import (
    DEFAULT_FRAME_ALIGNMENT,
    DEFAULT_HORIZONTAL_PADDING,
    DEFAULT_OUTER_WIDTH,
    DEFAULT_TEXT_ALIGNMENT,
    DEFAULT_TEXT_WRAP,
    DEFAULT_THEME,
    DEFAULT_VERTICAL_PADDING,
)
from .themes import Theme
from .utils import get_terminal_width


class Frame:
    def __init__(
        self,
        color: Color | None = None,
        text_alignment: Alignment = DEFAULT_TEXT_ALIGNMENT,
        alignment: Alignment = DEFAULT_FRAME_ALIGNMENT,
        theme: Theme = DEFAULT_THEME,
        horizontal_padding: int = DEFAULT_HORIZONTAL_PADDING,
        vertical_padding: int = DEFAULT_VERTICAL_PADDING,
        outer_width: int = DEFAULT_OUTER_WIDTH,
        container_width: int | None = None,
        colorize: Callable[[str], str] | None = None,
        wrap: Callable[[str, int], str] = DEFAULT_TEXT_WRAP,
    ) -> None:
        """
        Parameters:
            color: The color of the frame. Use this for colorization out
                of the box. For more sophistaced options, you can pass a
                colorization function to the parameter `colorize`.

            text_alignment: The alignment of the text inside the frame.

            alignment: The alignment of the frame inside the container.

            theme: The appearance of the frameline. Choose one the predefined
                themes from hemline.themes or build your own instance of
                hemline.themes.Theme.

            horizontal_padding: The number of whitespace characters used for
                horizontal padding.

            vertical_padding: The number of blank lines used for vertical
                padding.

            outer_width: The outer width of the Frame, including horizontal
                padding and the frame itself.

            container_width: The width of an imgainary container for the frame,
                resorts to the width of the terminal, if none is provided.

            colorize: A function to apply your custom colorization. Must take a
                string return the colorized string. Passing this will override
                any value provided to `color` parameter.

            wrap: A function to apply your custom wrapping logic. Must take a
                string and the width and return the wrapped string.
        """
        self.text_alignment = text_alignment
        self.alignment = alignment
        self.theme = theme
        self.horizontal_padding = horizontal_padding
        self.vertical_padding = vertical_padding
        self.outer_width = outer_width
        self.container_width = container_width
        if not color:
            self.colorize = colorize
        else:
            self.colorize = colorize or partial(default_colorize, color=color)
        self.wrap = wrap

    @property
    def effective_container_width(self) -> int:
        terminal_width = get_terminal_width()
        if self.container_width is None:
            return terminal_width

        return min(self.container_width, terminal_width)

    @property
    def effective_outer_width(self) -> int:
        return min(self.outer_width, self.effective_container_width)

    @property
    def inner_width(self) -> int:
        return self.effective_outer_width - 2

    @property
    def text_width(self) -> int:
        return self.inner_width - 2 * self.horizontal_padding

    @property
    def vertical_border(self) -> str:
        character = self.theme.vertical
        character = self.colorize(character) if self.colorize else character
        return character

    def format(self, text: str) -> str:
        """
        Parameters:
            text: The text to frame.
        """
        text = self.wrap(text, self.text_width)
        raw_lines = text.split("\n")
        raw_lines = (
            [""] * self.vertical_padding
            + raw_lines
            + [""] * self.vertical_padding
        )
        top_line = self._border_line(
            left=self.theme.top_left,
            right=self.theme.top_right,
        )
        bottom_line = self._border_line(
            left=self.theme.bottom_left,
            right=self.theme.bottom_right,
        )
        framed_lines = [self._framed_line(text=line) for line in raw_lines]
        return "\n".join([top_line] + framed_lines + [bottom_line])

    def _pad_line(self, line: str) -> str:
        return (
            " " * self.horizontal_padding + line + " " * self.horizontal_padding
        )

    def _apply_vertical_border(self, line: str) -> str:
        return self.vertical_border + line + self.vertical_border

    def _align_text(self, line: str) -> str:
        return get_alignment_method(self.text_alignment)(line, self.inner_width)

    def _align_framed_line(self, line: str) -> str:
        return get_alignment_method(self.alignment)(
            line, self.effective_container_width
        )

    def _border_line(
        self,
        left: str,
        right: str,
    ) -> str:
        line = left + self.inner_width * self.theme.horizontal + right
        line = self._align_framed_line(line)
        if self.colorize:
            return self.colorize(line)
        return line

    def _framed_line(self, text: str) -> str:
        text = self._pad_line(text)
        text = self._align_text(text)
        text = self._apply_vertical_border(text)
        text = self._align_framed_line(text)
        return text
