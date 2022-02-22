import sys
from pathlib import Path

from layer2svg import layer2svg, Mode

def main():
    if len(sys.argv) == 1:
        raise(ValueError("no args"))
    if len(sys.argv) >= 3:
        mode_str = sys.argv[-1]
        if mode_str == "layer":
            mode = Mode.layer
        elif mode_str == "build":
            mode = Mode.build
        elif mode_str == "number":
            mode = Mode.number
    else:
        mode = Mode.layer
    infile = sys.argv[1]
    layer2svg(Path(infile), mode=mode)

main()
