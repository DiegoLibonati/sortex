import tkinter as tk

import pytest


@pytest.fixture(scope="session")
def root() -> tk.Tk:
    instance: tk.Tk = tk.Tk()
    instance.withdraw()
    yield instance
    instance.destroy()
