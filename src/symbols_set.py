"""
* Utils for Fetching and Processing 'Set' Data
"""

# Local Imports
import os
from functools import cache
from pathlib import Path

# Third Party Imports
import requests
import yarl

# Local Imports
from src.constants import Paths, SetData
from src.types import SetDetails

"""
* Scryfall Data Utils
"""


@cache
def get_all_sets() -> dict[str, SetDetails]:
    """Make a GET request to the https://api.scryfall.com/sets endpoint.

    Returns:
        List of dictionaries containing set data.
    """
    sets = requests.get('https://api.scryfall.com/sets').json()
    return {n['code']: {
        'type': n['set_type'].lower(),
        'parent': n.get('parent_set_code', '').lower() or None,
        'icon': yarl.URL(n.get('icon_svg_uri', '')).with_suffix('').name.lower(),
        'name': n.get('name', '')
    } for n in sets.get('data', [])}


"""
* Set Symbol Utils
"""


def get_sets_by_symbol(sym: str) -> dict[str, SetDetails]:
    """Return a list of set codes that use a given SVG symbol.

    Args:
        sym: The name of an SVG set symbol recognized by Scryfall.

    Returns:
        A list of Scryfall 'set' objects that use the given symbol.
    """
    return {code: v for code, v in get_all_sets().items() if sym.lower() in v['icon']}


def check_code_recognized(code: str) -> tuple[bool, str]:
    """Check if a symbol code is recognized.

    Args:
        code: Symbol code to look for.

    Returns:
        Tuple containing a bool check (whether code was recognized) and
            the proper symbol code for the code given.
    """
    code_formatted = code.upper()

    # Skip this if it's in the reroutes
    if code_formatted in SetData.ROUTES:
        return True, SetData.ROUTES[code_formatted].lower()

    # Skip this set if we have it in the SVG library
    if Path(Paths.SET, code_formatted).is_dir():
        return True, code

    # Default to code
    return False, code


"""
* Set Symbol Checks
"""


def get_unused_vectors_set() -> set[str]:
    """Get a set (non-repeating list) of symbols in the repository not used by any known Scryfall 'Set' object."""
    return {
        # Get all icon directories not present in Scryfall icon list
        n for n in os.listdir(Paths.SET)
        if n not in set([
            # Get all icons present in Scryfall 'Set' data
            yarl.URL(n['icon']).with_suffix('').name.upper()
            for code, n in get_all_sets().items()]
        ) and n not in SetData.IGNORED
    }
