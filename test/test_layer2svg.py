""
from pathlib import Path
from layer2svg import layer2svg, Mode
import re

DIR = Path(__file__).parent 
IN = DIR / "circles.svg"

def count_circles(fn: Path) -> int:
    "counts the numbers of circles in the svg file"
    svg_data = fn.read_text("utf-8")
    matches = re.findall(r"<\S*?ellipse.*?\/>", svg_data, re.DOTALL)
    return len(matches)

def test_layer():
    layer2svg(IN, DIR / "layers")
    results = {
        p: count_circles(p) for p in (DIR / "layers").iterdir()
    }
    assert len(results) == 4
    assert results[DIR / "layers" / "asdf 1.svg"] == 6
    assert results[DIR / "layers" / "asdf 2.svg"] == 7
    assert results[DIR / "layers" / "asdf 3.svg"] == 8
    assert results[DIR / "layers" / "3.svg"] == 9


def test_build():
    layer2svg(IN, DIR / "build", Mode.build)
    results = {
        p: count_circles(p) for p in (DIR / "build").iterdir()
    }
    assert len(results) == 5
    assert results[DIR / "build" / "1.svg"] == 5
    assert results[DIR / "build" / "2.svg"] == 6
    assert results[DIR / "build" / "3.svg"] == 8
    assert results[DIR / "build" / "4.svg"] == 11
    assert results[DIR / "build" / "5.svg"] == 15
if __name__ == "__main__":
    test_build()
