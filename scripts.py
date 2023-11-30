"""
* MTG Vectors
* Data Gathering and Testing Scripts
"""
# Standard Library Imports
import os
from pathlib import Path
from pprint import pprint
from typing import Union

# Third Party Imports
import requests
import yaml

# Empty data objects
ROUTES_SET = {}
MISSING_SET = {}
IGNORED_SET = []

# Paths
PATH_ROOT = Path(os.getcwd())
PATH_SET = PATH_ROOT / 'svg' / 'set'
PATH_DATA = PATH_ROOT / 'data'
PATH_ROUTES_SET = PATH_DATA / 'routes.set.yml'
PATH_IGNORE_SET = PATH_DATA / 'ignored.set.yml'
PATH_MISSING_SET = PATH_DATA / 'missing.set.yml'

"""
* UTIL Funcs
"""


def load_data_file(path: Path) -> Union[list, dict]:
    """Return a loaded object from a given data file.

    Args:
        path: Path to the data file (YAML only).

    Returns:
        Loaded object (a list or a dict).
    """
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.Loader)


"""
* Funcs
"""


def get_all_sets() -> list[dict]:
    """Make a GET request to the https://api.scryfall.com/sets endpoint.

    Returns:
        List of dictionaries containing set data.
    """
    sets = requests.get('https://api.scryfall.com/sets').json()
    return [{
        'type': n['set_type'],
        'code': n['code'],
        'parent': n.get('parent_set_code'),
        'icon': n.get('icon_svg_uri', ''),
        'name': n.get('name', '')
    } for n in sets.get('data', []) if 'set_type' in n and 'code' in n]


def get_defined_sets() -> tuple[list[str], dict[str, str]]:
    """Get a list of all defined sets and a list of replacement sets."""
    return [
        # All set codes
        n.lower() for n in list(ROUTES_SET.keys())
    ], {
        # All sets to replace with a parent code
        k.lower(): v.lower() for k, v
        in ROUTES_SET.items()
        if isinstance(v, str) and len(v) > 1
    }


def get_missing_vectors_set() -> tuple[dict[str, list[str]], dict[str, dict[str, list[str]]]]:
    """Get a tuple containing all the child and parent sets known to Scryfall that don't have a matching vector
    symbol catalogued in this repository."""
    missing_children, missing_parents = {}, {}
    sets, parents = get_defined_sets()
    all_sets = get_all_sets()

    # Iterate through each set in the JSON data
    for n in all_sets:

        # Ignore known missing sets
        if n['code'].upper() in MISSING_SET:
            continue

        # Replace problematic windows names
        if n['code'] == 'con':
            n['code'] = 'conf'

        # Skip token sets
        if n['type'] in ['token', 'minigame']:
            continue

        # Ignore theme card sets
        if n['type'] in ['memorabilia'] and 'Front Cards' in n['name']:
            continue

        # Skip this set if we have it in the SVG library
        if Path(PATH_SET, n['code'].upper()).is_dir():
            continue

        # Skip if set routes to a parent present in the SVG library
        parent_set = parents.get(n['code'], '').upper()
        if parent_set and Path(PATH_SET, parent_set).is_dir():
            continue

        # Promo sets with parent
        if len(n['code']) > 3 and n['parent']:

            # Skip promo sets with known parent, e.g. pMID -> MID
            short = n['code'][1:]
            if n['parent'] == short and Path(PATH_SET, short.upper()).is_dir():
                continue

            # Skip promo token sets with known parent, e.g. ptSNC -> SNC
            short = n['code'][2:]
            if n['parent'][1:] == short and Path(PATH_SET, short.upper()).is_dir():
                continue

        # Add missing set without a parent
        if not n['parent']:
            missing_parents.setdefault(n['type'], []).append((n['code'], n['icon']))
            continue

        # Add missing parents
        missing_children.setdefault(n['type'], {})
        missing_children[n['type']].setdefault(n['parent'], []).append((n['code'], n['icon']))

    # Return missing
    return missing_parents, missing_children


def get_unused_vectors_set() -> set[str]:
    """Get a set (non-repeating list) of symbols in the repository not used by any known Scryfall 'Set' object."""
    sets = set([n['code'] for n in get_all_sets()])
    return {
        n for n in os.listdir(PATH_SET)
        if not n.lower() in sets and n not in IGNORED_SET
    }


def get_sets_by_symbol(sym: str) -> list[dict]:
    """Return a list of set codes that use a given SVG symbol.

    Args:
        sym: The name of an SVG set symbol recognized by Scryfall.

    Returns:
        A list of Scryfall 'set' objects that use the given symbol.
    """
    return [v for v in get_all_sets() if sym.lower() in v['icon']]


def analyze_missing_vectors_set() -> None:
    """Analyze any sets that don't have a matching vector symbol found in this repository.

    Notes:
        Provides printed user feedback on top of the functionality of 'get_missing_vectors_set'.
    """
    # Get any missing sets
    sets_missing, parents_missing = get_missing_vectors_set()

    # Missing parent sets
    if sets_missing:
        print("MAIN PARENT SETS:")
        pprint(sets_missing)

    # Missing child sets
    if parents_missing:
        print("="*80)
        print("="*80)
        print("MISSING CHILDREN SETS:")
        pprint(parents_missing)

    # All good
    if not sets_missing and not parents_missing:
        print("NO SETS MISSING!")


"""
* Launch Script
"""

if __name__ == '__main__':

    # Load our data
    ROUTES_SET = load_data_file(PATH_ROUTES_SET)
    IGNORED_SET = load_data_file(PATH_IGNORE_SET)
    MISSING_SET = load_data_file(PATH_MISSING_SET).get('missing', [])

    # Analyze missing sets
    analyze_missing_vectors_set()
