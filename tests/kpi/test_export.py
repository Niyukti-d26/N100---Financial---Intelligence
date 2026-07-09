from pathlib import Path

from src.screener.engine import ScreenerEngine
from src.screener.export import export_screeners


def test_export():

    engine = ScreenerEngine()

    path = export_screeners(engine)

    assert Path(path).exists()