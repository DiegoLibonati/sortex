from tkinter import CENTER, DISABLED, FLAT, NORMAL, W

from src.ui.styles import Styles


class TestStyles:
    def test_primary_color(self) -> None:
        assert Styles.PRIMARY_COLOR == "#250001"

    def test_white_color(self) -> None:
        assert Styles.WHITE_COLOR == "#FFFFFF"

    def test_black_color(self) -> None:
        assert Styles.BLACK_COLOR == "#000000"

    def test_white_smoke_color(self) -> None:
        assert Styles.WHITE_SMOKE_COLOR == "#F3F3F3"

    def test_font_arial_base(self) -> None:
        assert Styles.FONT_ARIAL == "Arial"

    def test_font_arial_10(self) -> None:
        assert Styles.FONT_ARIAL_10 == "Arial 10"

    def test_font_arial_12(self) -> None:
        assert Styles.FONT_ARIAL_12 == "Arial 12"

    def test_font_arial_bold_10(self) -> None:
        assert Styles.FONT_ARIAL_BOLD_10 == "Arial 10 bold"

    def test_font_arial_bold_12(self) -> None:
        assert Styles.FONT_ARIAL_BOLD_12 == "Arial 12 bold"

    def test_font_arial_bold_20(self) -> None:
        assert Styles.FONT_ARIAL_BOLD_20 == "Arial 20 bold"

    def test_center_matches_tkinter(self) -> None:
        assert Styles.CENTER == CENTER

    def test_anchor_center_matches_tkinter(self) -> None:
        assert Styles.ANCHOR_CENTER == CENTER

    def test_relief_flat_matches_tkinter(self) -> None:
        assert Styles.RELIEF_FLAT == FLAT

    def test_state_normal_matches_tkinter(self) -> None:
        assert Styles.STATE_NORMAL == NORMAL

    def test_state_disabled_matches_tkinter(self) -> None:
        assert Styles.STATE_DISABLED == DISABLED

    def test_anchor_w_matches_tkinter(self) -> None:
        assert Styles.ANCHOR_W == W

    def test_cursor_hand2(self) -> None:
        assert Styles.CURSOR_HAND2 == "HAND2"
