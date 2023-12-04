"""
* MTG Vectors
* Data Gathering and Testing Scripts
"""
# Standard Library Imports
import os
from pathlib import Path
from pprint import pprint
from typing import Union, Optional, TypedDict

# Third Party Imports
import requests
import yaml
import yarl

# Empty data objects
CORRECTED_SET = {}
EMPTY_SET = []
IGNORED_SET = []
MISSING_SET = []
MIXED_SET = []
ROUTES_SET = {}

# Paths
PATH_ROOT = Path(os.getcwd())
PATH_SET = PATH_ROOT / 'svg' / 'set'
PATH_DATA = PATH_ROOT / 'data'
PATH_ALIAS_SET = PATH_DATA / 'alias.set.yml'
PATH_CORRECTED_SET = PATH_DATA / 'corrected.set.yml'
PATH_EMPTY_SET = PATH_DATA / 'empty.set.yml'
PATH_IGNORED_SET = PATH_DATA / 'ignored.set.yml'
PATH_MISSING_SET = PATH_DATA / 'missing.set.yml'
PATH_MIXED_SET = PATH_DATA / 'mixed.set.yml'
PATH_ROUTES_SET = PATH_DATA / 'routes.set.yml'


class SetDetails(TypedDict):
    """Set details dictionary."""
    type: str
    code: str
    parent: Optional[str]
    icon: str
    name: str


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


def get_all_sets() -> list[SetDetails]:
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
    sets = set([yarl.URL(n['icon']).with_suffix('').name.upper() for n in get_all_sets()])
    return {
        n for n in os.listdir(PATH_SET)
        if n not in sets and n not in IGNORED_SET
    }


def get_sets_by_symbol(sym: str) -> list[SetDetails]:
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


def get_symbol_code(code: str, parent: Optional[str]) -> Optional[str]:
    """Look for the system appropriate symbol code for a given set code with optional parent code.

    Args:
        code: 3-5 letter set code.
        parent: 3-5 letter set code of the parent set, if required.

    Returns:
        Best guess at the appropriate matching symbol code based on the available data files.
    """

    # Replace problematic windows names
    if code == 'CON':
        return 'conf'

    # Skip this if it's in the reroutes
    if code in ROUTES_SET:
        return ROUTES_SET[code]

    # Skip this set if we have it in the SVG library
    if Path(PATH_SET, code).is_dir():
        return code

    # Skip if set routes to a parent present in the SVG library
    if parent and Path(PATH_SET, parent).is_dir():
        return parent

    # Skip if set's parent is present in the reroutes
    if parent and parent in ROUTES_SET:
        return ROUTES_SET[parent]

    # Promo sets with parent
    if len(code) > 3 and parent:

        # Skip promo sets with known parent, e.g. pMID -> MID
        short = code[1:]
        if short == 'CON':
            return 'conf'
        if parent == short:
            return get_symbol_code(short, None)

        # Skip promo token sets with known parent, e.g. ptSNC -> SNC
        short = code[2:]
        if short == 'CON':
            return 'conf'
        if parent[1:] == short:
            return get_symbol_code(short, None)

    # Default to code
    return code


def compare_sets_and_symbols() -> list[tuple[str, Optional[str], str]]:
    """Checks the symbol icon of every set against the current defined symbol code for that set."""
    results = []
    sets = get_all_sets()
    for data in sets:

        # Skip sets with no symbol or mixed symbols
        if data['code'].upper() in EMPTY_SET or data['code'].upper() in MIXED_SET:
            continue

        # Skip irrelevant non-playable cards
        if data['type'] in ['minigame', 'token']:
            continue
        if data['type'] == 'memorabilia' and 'Front Cards' in data['name']:
            continue

        # Get the Scryfall appropriate symbol name
        symbol = yarl.URL(data['icon']).with_suffix('').name.lower()
        if data['code'].upper() in CORRECTED_SET:
            symbol = CORRECTED_SET.get(data['code'].upper()).lower()

        # Get the currently established symbol name
        current = get_symbol_code(data['code'].upper(), data['parent'].upper() if data['parent'] else None).lower()
        if current == 'conf':
            continue
        if symbol.upper() in ALIAS_SET.get(current.upper(), []):
            continue

        # Established symbol name doesn't match the Scryfall name
        if symbol != current:
            results.append((data['code'], current, symbol))
    return results


"""
* Launch Script
"""

if __name__ == '__main__':

    # Load our data
    ALIAS_SET = load_data_file(PATH_ALIAS_SET)
    CORRECTED_SET = load_data_file(PATH_CORRECTED_SET)
    EMPTY_SET = load_data_file(PATH_EMPTY_SET).get('empty', [])
    IGNORED_SET = load_data_file(PATH_IGNORED_SET).get('ignored', [])
    MISSING_SET = load_data_file(PATH_MISSING_SET)
    MIXED_SET = load_data_file(PATH_MIXED_SET).get('mixed', [])
    ROUTES_SET = load_data_file(PATH_ROUTES_SET)

    # Check misnamed symbol codes
    print("MISNAMED SYMBOLS:")
    print("=" * 120)
    pprint(compare_sets_and_symbols())
    print("=" * 120)

    # Get unused set symbols
    print("UNUSED SYMBOLS:")
    print("=" * 120)
    pprint(get_unused_vectors_set())
    print("=" * 120)

    # Analyze missing sets
    analyze_missing_vectors_set()
