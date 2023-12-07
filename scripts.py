"""
* MTG Vectors
* Data Gathering and Testing Scripts
"""
# Standard Library Imports
import os
from pathlib import Path
from pprint import pprint

# Local Imports
from src.symbols_set import get_all_sets, check_code_recognized
from src.types import SetManifest
from src.utils import dump_data_file, create_zip
from src.constants import Constants, Paths, SetPath, SetData, URI

"""
* Analysis Scripts
"""


def get_missing_symbols_set() -> dict[str, list[str]]:
    """Get a tuple containing all the child and parent sets known to Scryfall that don't have a matching vector
    symbol catalogued in this repository."""
    all_sets, missing = get_all_sets(), {}

    # Iterate through each set in the JSON data
    for code, n in all_sets.items():

        # Check if the set code is accounted for
        check, _ = check_code_recognized(code)
        if check:
            continue

        # Check if the set icon is accounted for
        check, _ = check_code_recognized(n['icon'])
        if check:
            continue

        # Add missing set
        missing.setdefault(n['icon'].upper(), []).append(code)

    # Return missing
    return missing


def analyze_missing_symbols_set() -> None:
    """Analyze any sets that don't have a matching vector symbol found in this repository.

    Notes:
        Provides printed user feedback on top of the functionality of 'get_missing_vectors_set'.
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


"""
* Build Scripts
"""


def generate_manifest() -> None:
    """Generates a manifest of all symbols in the repository."""
    manifest: SetManifest = {
        'meta': {
            'date': Constants.DATE_NOW,
            'version': Constants.VERSION_FULL,
            'uri': URI.PKG_SET,
            'routes': SetData.ROUTES.copy()
        },
        'symbols': {}
    }

    # Determine the supported rarities in each symbol directory
    for folder in os.listdir(Paths.SET):
        # Ignored folders
        if folder in ['.alt', '.extras']:
            continue
        # Add rarities to manifest
        manifest['symbols'][folder] = [
            Path(svg).stem for svg in
            os.listdir(Path(Paths.SET, folder))
            if svg.upper().strip('.svg') not in SetData.RARITIES]

    # Sort manifest symbols and dump data file
    manifest['symbols'] = dict(sorted(manifest['symbols'].items())).copy()
    dump_data_file(manifest, SetPath.MANIFEST, config={'sort_keys': False})

    # Create a zip ofd all symbols
    create_zip(Paths.SET, Path(Paths.PKG, 'set.zip'))


"""
* Launch Script
"""

if __name__ == '__main__':

    # Load our data
    analyze_missing_symbols_set()
