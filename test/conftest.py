from tkinter import BooleanVar, IntVar, StringVar
from unittest.mock import MagicMock

import pytest

from src.ui.styles import Styles


@pytest.fixture
def mock_root() -> MagicMock:
    root: MagicMock = MagicMock()
    root.title = MagicMock()
    root.geometry = MagicMock()
    root.resizable = MagicMock()
    root.config = MagicMock()
    root.columnconfigure = MagicMock()
    root.rowconfigure = MagicMock()
    return root


@pytest.fixture
def mock_styles() -> MagicMock:
    styles: MagicMock = MagicMock()
    styles.PRIMARY_COLOR = "#250001"
    styles.WHITE_COLOR = "#FFFFFF"
    styles.BLACK_COLOR = "#000000"
    styles.WHITE_SMOKE_COLOR = "#F3F3F3"
    styles.FONT_ARIAL_BOLD_10 = "Arial 10 bold"
    styles.RELIEF_FLAT = "flat"
    styles.STATE_NORMAL = "normal"
    styles.STATE_DISABLED = "disabled"
    styles.CURSOR_HAND2 = "HAND2"
    styles.ANCHOR_W = "w"
    styles.ANCHOR_CENTER = "center"
    return styles


@pytest.fixture
def real_styles() -> Styles:
    return Styles()


@pytest.fixture
def mock_on_search() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_on_organize() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_on_revert() -> MagicMock:
    return MagicMock()


@pytest.fixture
def variable() -> MagicMock:
    return MagicMock(spec=StringVar)


@pytest.fixture
def bool_variable() -> MagicMock:
    return MagicMock(spec=BooleanVar)


@pytest.fixture
def int_variable() -> MagicMock:
    return MagicMock(spec=IntVar)


@pytest.fixture
def mock_file_organizer() -> MagicMock:
    organizer: MagicMock = MagicMock()
    organizer.extensions_allowed = []
    organizer.filters = {}
    return organizer
