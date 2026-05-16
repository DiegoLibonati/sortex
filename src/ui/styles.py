from typing import Final, Literal


class Styles:
    PRIMARY_COLOR = "#250001"
    WHITE_COLOR = "#FFFFFF"
    BLACK_COLOR = "#000000"
    WHITE_SMOKE_COLOR = "#F3F3F3"

    FONT_ARIAL = "Arial"
    FONT_ARIAL_10 = f"{FONT_ARIAL} 10"
    FONT_ARIAL_12 = f"{FONT_ARIAL} 12"
    FONT_ARIAL_13 = f"{FONT_ARIAL} 13"
    FONT_ARIAL_14 = f"{FONT_ARIAL} 14"
    FONT_ARIAL_15 = f"{FONT_ARIAL} 15"
    FONT_ARIAL_20 = f"{FONT_ARIAL} 20"

    FONT_ARIAL_BOLD_10 = f"{FONT_ARIAL} 10 bold"
    FONT_ARIAL_BOLD_12 = f"{FONT_ARIAL} 12 bold"
    FONT_ARIAL_BOLD_13 = f"{FONT_ARIAL} 13 bold"
    FONT_ARIAL_BOLD_14 = f"{FONT_ARIAL} 14 bold"
    FONT_ARIAL_BOLD_15 = f"{FONT_ARIAL} 15 bold"
    FONT_ARIAL_BOLD_20 = f"{FONT_ARIAL} 20 bold"

    CENTER: Final[Literal["center"]] = "center"

    ANCHOR_CENTER: Final[Literal["center"]] = "center"

    RELIEF_FLAT: Final[Literal["flat"]] = "flat"

    STATE_NORMAL: Final[Literal["normal"]] = "normal"
    STATE_DISABLED: Final[Literal["disabled"]] = "disabled"

    CURSOR_HAND2 = "hand2"

    ANCHOR_W: Final[Literal["w"]] = "w"
