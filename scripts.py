"""
* MTG Vectors
* Data Gathering and Testing Scripts
"""
# Standard Library Imports
import os
from pathlib import Path
from pprint import pprint

# Local Imports
from src.constants import Constants, Paths, SetData, URI, SetRarities
from src.symbols_set import get_missing_symbols_set, get_missing_symbols_set_rarities
from src.symbols_wm import get_missing_symbols_watermark, get_local_watermarks
from src.types import Manifest
from src.utils import dump_data_file, create_zip


"""
* Analysis Scripts
"""


def analyze_missing_symbols_set() -> None:
    """Analyze any sets that don't have a matching vector symbol found in this repository.

    Notes:
        Provides printed user feedback on top of the functionality of 'get_missing_symbols_set'.
    """
    # Get any missing sets
    missing = get_missing_symbols_set()

    # Missing parent sets
    if missing:
        print("=" * 50)
        print("Missing Symbols and Matching Sets:")
        print("=" * 50)
        pprint(missing, width=50)
        return

    # All good
    print("=" * 50)
    print("NO SETS MISSING!")
    print("=" * 50)


def analyze_missing_symbols_watermark() -> None:
    """Analyze any watermarks that don't have a matching vector symbol found in this repository.

    Notes:
        Provides printed user feedback on top of the functionality of 'get_missing_symbols_watermark'.
    """
    # Get any missing sets
    missing = get_missing_symbols_watermark()

    # Missing parent sets
    if missing:
        print("=" * 50)
        print("Missing Symbols and Matching Sets:")
        print("=" * 50)
        pprint(missing, width=50)
        return

    # All good
    print("=" * 50)
    print("NO SETS MISSING!")
    print("=" * 50)


def generate_markdown_missing() -> None:
    """Generates the 'MISSING.md' file used in this repository."""
    missing_set = [(k.upper(), v[0].lower()) for k, v in get_missing_symbols_set().items()]
    missing_rarities = get_missing_symbols_set_rarities()
    missing_wm = get_missing_symbols_watermark()

    # Add to MD file
    with open(Paths.MD_MISSING, 'w', encoding='utf-8') as file:
        file.write('# Missing Set Symbols\n')
        file.write('| Symbol Code   | Links         |\n')
        file.write('| ------------- | ------------- |\n')
        for symbol, code in missing_set:
            file.write(f'| {symbol.upper()} |'
                       f'[SVG](https://svgs.scryfall.io/sets/{symbol.lower()}.svg), '
                       f'[Cards](https://scryfall.com/sets/{code.lower()}) |\n')
        file.write('\n# Missing Watermarks\n')
        file.write('| Symbol Name   | Links         |\n')
        file.write('| ------------- | ------------- |\n')
        for wm in missing_wm:
            file.write(f'| {wm.title()} |'
                       f'[Cards](https://scryfall.com/search?q=watermark%3A{wm.lower()}) |\n')
        file.write('\n# Missing Set Symbol Rarities\n')
        file.write('| Symbol Name   | Rarities Missing | Links |\n')
        file.write('| ------------- | ---------------- | ----- |\n')
        for symbol, missing in missing_rarities:
            file.write(f'| {symbol.upper()} '
                       f'| {missing} |'
                       f'[SVG](https://svgs.scryfall.io/sets/{symbol.lower()}.svg), '
                       f'[Cards](https://scryfall.com/sets/{code.lower()}) |\n')


"""
* Build Scripts
"""


def generate_manifest() -> None:
    """Generates a manifest of all symbols in the repository."""
    manifest: Manifest = {
        'meta': {
            'date': Constants.DATE_NOW,
            'version': Constants.VERSION_FULL,
            'uri': URI.PACKAGE
        },
        'set': {
            'routes': SetData.ROUTES.copy(),
            'rarities': SetRarities.copy(),
            'symbols': {}
        },
        'watermark': {
            'routes': {},
            'symbols': []
        }
    }

    # Determine the supported rarities in each symbol directory
    for folder in os.listdir(Paths.SET):
        # Ignored folders
        if folder in ['.alt', '.extras']:
            continue
        # Add rarities to manifest
        manifest['set']['symbols'][folder] = [
            Path(svg).stem for svg in
            os.listdir(Path(Paths.SET, folder))
            if svg.upper().strip('.svg') not in SetData.RARITIES]

    # Sort Set Symbols
    manifest['set']['symbols'] = dict(sorted(manifest['set']['symbols'].items())).copy()

    # Create a sorted list of watermarks
    manifest['watermark']['symbols'] = sorted(get_local_watermarks())

    # Dump manifest file
    dump_data_file(manifest, Paths.MANIFEST, config={'sort_keys': False})

    # Create a zip of all symbols
    create_zip(Paths.SVG, Paths.PACKAGE)


"""
* Launch Script
"""

if __name__ == '__main__':

    # Load our data
    generate_markdown_missing()
