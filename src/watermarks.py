"""
* Utils for Fetching and Processing 'Set' Data
"""
# Standard Library Imports
import os
from functools import cache
from pathlib import Path

# Third Party Imports
import requests

# Local Imports
from src.constants import Paths, WMData

"""
* Get Watermark Data
"""


@cache
def get_all_watermarks() -> list[str]:
    """Returns a list of all watermarks found in Scryfall's watermarks catalog."""
    return requests.get('https://api.scryfall.com/catalog/watermarks').json().get('data', [])


@cache
def get_local_watermarks() -> list[str]:
    """Returns a list of all watermark names accounted for in this repository."""
    return [
        Path(Paths.WATERMARK, n).stem.lower()
        for n in os.listdir(Paths.WATERMARK) if n.endswith('.svg')
    ]


"""
* Watermark Checks
"""


def get_unused_watermarks() -> list[str]:
    """Returns a list of all watermarks in this repository not found in the Scryfall catalog."""
    watermarks = get_all_watermarks()
    return [wm for wm in get_local_watermarks() if wm not in watermarks]


def get_missing_watermarks() -> list[str]:
    """Returns a list of all watermarks in Scryfall's catalog not found in this repository."""
    local_wm = get_local_watermarks()
    ignore_list = [*local_wm, *WMData.IGNORED]
    return [wm for wm in get_all_watermarks() if wm not in ignore_list]
