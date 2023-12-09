"""
* Utils for Fetching and Processing 'Set' Data
"""
# Standard Library Imports
import os
from functools import cache

# Third Party Imports
import requests

# Local Imports
from src.constants import Paths

"""
* Scryfall Data Utils
"""


@cache
def get_all_watermarks() -> list[str]:
    """Make a GET request to the https://api.scryfall.com/catalog/watermarks endpoint.

    Returns:
        List of watermarks found in Scryfall's watermarks catalog.
    """
    wm_list = requests.get('https://api.scryfall.com/catalog/watermarks').json().get('data', [])
    if 'set' in wm_list:
        wm_list.remove('set')
    return wm_list


"""
* Watermark Symbol Utils
"""


def get_local_watermarks() -> list[str]:
    """list[str]: Returns a list of all watermark names accounted for in this repository."""
    return [p.lower().replace('.svg', '') for p in os.listdir(Paths.WATERMARK) if '.svg' in p.lower()]


"""
* Watermark Symbol Checks
"""


def get_unused_symbols_watermark() -> list[str]:
    """list[str]: Returns a list of all watermarks in this repository not found in the Scryfall catalog."""
    watermarks = get_all_watermarks()
    return [wm for wm in get_local_watermarks() if wm not in watermarks]


def get_missing_symbols_watermark() -> list[str]:
    """list[str]: Returns a list of all watermarks in Scryfall's catalog not found in this repository."""
    local_wm = get_local_watermarks()
    return [wm for wm in get_all_watermarks() if wm not in local_wm]
