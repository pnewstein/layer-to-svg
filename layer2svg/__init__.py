#! /usr/bin/env python
import xml.etree.ElementTree as ET
import os
from pathlib import Path
import copy
import sys
from enum import Enum
from typing import Optional

class Mode(Enum):
    layer = 0
    build = 1
    number = 2

def clear_background(all_layers: list[str], verbose: Optional[bool]=None) -> tuple[list[str], list[str]]:
    """
    removes all layers with the name background from the layer
    returns the remaining layers and the background layers as two lists of strings
    Verbose flag defines whether to add debug information and defaults to false
    """
    if verbose is None:
        verbose = False

    al_copy = copy.deepcopy(all_layers)
    background_layers = [layer for layer in al_copy if "background" in layer.lower()]
    if len(background_layers) == 0:
        print("No background")
    for layer in background_layers:
        al_copy.remove(layer)
    return al_copy, background_layers

def get_layers_to_remove(root: ET.ElementTree, mode: Mode, verbose: Optional[bool]=None
                         ) -> dict[str, list[str]]:
    """
    returns a dict with the name of the file plus the list of layer names to delete
    if verbose is True, print out the layers
    """
    if verbose is None:
        verbose = False
    all_layers_null = [
        g.get('{http://www.inkscape.org/namespaces/inkscape}label')
        for g in root.findall('{http://www.w3.org/2000/svg}g')
    ]
    for layer in all_layers_null:
        if layer is None:
            raise ValueError("Layer parse failure")
    all_layers: list[str] = all_layers_null # type: ignore

    if verbose:
        print(all_layers)

    out: dict[str, list[str]] = {}
    if mode == Mode.layer:
        # remove background layers
        all_layers, _ = clear_background(all_layers, verbose=verbose)

        # build out
        for layer in all_layers:
            layers_copy = copy.deepcopy(all_layers)
            layers_copy.remove(layer)
            out[layer] = layers_copy

    if mode == Mode.build:
        for i, _ in enumerate(all_layers):
            layers_copy = copy.deepcopy(list(reversed(all_layers)))
            out[str(len(all_layers) - i)] = layers_copy[:i]

    if mode == Mode.number:
        # remove background layers
        all_layers, _ = clear_background(all_layers, verbose=verbose)

        # build out
        for num in "1234567890":
            layers_copy = copy.deepcopy(all_layers)
            layers_to_keep = [l for l in all_layers if num in l]
            # there are no layers with that number
            if len(layers_to_keep) == 0:
                continue
            for l_to_keep in layers_to_keep:
                layers_copy.remove(l_to_keep)
            out[num] = layers_copy
    return out

def write_layers(layers_to_remove: dict[str, list[str]], tree: ET.ElementTree, export_folder: Path):
    for file_name, layers in layers_to_remove.items():
        for lname in layers:
            if len( lname ) == 1:
                lname = 'char_' + str(ord( lname ))
        temp_tree = copy.deepcopy(tree)
        temp_root = temp_tree.getroot()
        for g in temp_root.findall('{http://www.w3.org/2000/svg}g'):
            name = g.get('{http://www.inkscape.org/namespaces/inkscape}label')
            if name in layers:
                temp_root.remove(g)
            else:
                style = g.get('style')
                if type(style) is str:
                    style = style.replace( 'display:none', 'display:inline' )
                    g.set('style', style)
        temp_tree.write((export_folder / file_name).with_suffix(".svg"))

def layer2svg(file_path: Path, export_folder: Optional[Path] = None, mode: Optional[Mode] = None): 
    if export_folder is None:
        export_folder = Path() / file_path.with_suffix("").name
    if mode is None:
        mode = Mode.layer

    tree = ET.parse(file_path)
    layers_to_remove = get_layers_to_remove(tree, mode)
    print(layers_to_remove)
    export_folder.mkdir(exist_ok=True)
    write_layers(layers_to_remove, tree, export_folder)


def main():
    layer2svg(Path(sys.argv[1]))

if __name__ == '__main__':
    main()

