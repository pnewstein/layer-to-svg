import sys
from pathlib import Path
import argparse

from layer2svg import layer2svg, Mode

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The svg file to process")
    parser.add_argument("-o", "--out-directory", help="The directory where the output svgs are put. "
                        "Defaults to a folder with the same name as the input file",
                        default=None)
    mode_arg = parser.add_mutually_exclusive_group()
    mode_arg.add_argument("-l", "--layer", 
                          help="Use layer mode: each layer not containing the word background is stored as a separate svg",
                          action="store_true")
    mode_arg.add_argument("-b", "--build", 
                          help="Use build mode: layers are build on top of each other",
                          action="store_true")
    mode_arg.add_argument("-n", "--number", 
                          help="Use number mode: layers containing a number are combined into a svg for each number",
                          action="store_true")
    args = parser.parse_args()
    if args.build == True:
        mode = Mode.build
    elif args.number == True:
        mode = Mode.number
    else:
        mode = Mode.layer
    if args.out_directory is not None:
        export_folder = Path(args.out_directory)
    else:
        export_folder = None
    layer2svg(Path(args.file), export_folder=export_folder, mode=mode)

main()
