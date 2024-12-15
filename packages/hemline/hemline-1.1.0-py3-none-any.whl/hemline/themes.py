from typing import TypeAlias

SingleCharacter: TypeAlias = str


class Theme:
    def __init__(
        self,
        horizontal: SingleCharacter,
        vertical: SingleCharacter,
        top_left: SingleCharacter,
        top_right: SingleCharacter,
        bottom_left: SingleCharacter,
        bottom_right: SingleCharacter,
    ) -> None:
        """
        Parameters:
            horizontal: single character string.
            vertical: single character string.
            top_left: single character string.
            top_right: single character string.
            bottom_left: single character string.
            bottom_right: single character string.
        """
        self.horizontal = horizontal
        self.vertical = vertical
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        for field in [
            "horizontal",
            "vertical",
            "top_left",
            "top_right",
            "bottom_left",
            "bottom_right",
        ]:
            border = self.__validate_border(field)
            setattr(self, field, border)

    def __validate_border(self, field: str) -> str:
        border = getattr(self, field)
        if not isinstance(border, str):
            raise TypeError(f"Delimiter border `{field}` must be a string.")

        length = len(border)
        if not length == 1:
            raise ValueError(
                "Delimiters must be single characters. "
                f'`{field}` ("{border}") has {length}.'
            )
        return border


def factory(
    character: SingleCharacter, corner: SingleCharacter | None = None
) -> Theme:
    """Convenience factory for a Theme built from one character, optionally
    specifying the character used for corners.

    Parameters:
        character: The character to use for the frameline. Must be a
            single-character string.

        corner: The character to use for the corners, resorts to `character` if
            none is provided. Must be a single-character string.
    """
    corner = corner or character

    return Theme(
        horizontal=character,
        vertical=character,
        top_left=corner,
        top_right=corner,
        bottom_left=corner,
        bottom_right=corner,
    )


single: Theme = Theme(
    horizontal="─",
    vertical="│",
    top_left="┌",
    top_right="┐",
    bottom_left="└",
    bottom_right="┘",
)
double: Theme = Theme(
    horizontal="═",
    vertical="║",
    top_left="╔",
    top_right="╗",
    bottom_left="╚",
    bottom_right="╝",
)
dotted = factory("·")
none = factory(" ")
