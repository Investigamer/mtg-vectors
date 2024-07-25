"""
* Utils for Fetching and Processing 'Set' Data
"""
# Local Imports
import os
from functools import cache

# Third Party Imports
from hexproof import scryfall as Scryfall

# Local Imports
from src.constants import Paths, SetData
from src.schema import SetDetails, Icon

"""
* Icon Routing
"""


@cache
def get_icon_alias(icon: str) -> str:
    """Takes in a Scryfall icon and returns the MTG Vectors recognized icon code, using an alias if defined.

    Args:
        icon (str): Icon code provided by Scryfall.

    Returns:
        str: MTG-Vectors recognized icon code.
    """
    icon = icon.upper().strip()
    alias = SetData.ALIAS.get(icon)
    if alias is not None:
        return alias.upper().strip()
    return icon


@cache
def get_set_icon(set_code: str, icon: str) -> str:
    """Checks if a scryfall set code must be rerouted to a different icon.

    Args:
        set_code: Scryfall set code to check for defined routes.
        icon: Icon to check for alias, and return if no route or alias exists.

    Returns:
        The best-case icon definition for this set_code.
    """
    set_code = set_code.upper()
    if set_code in SetData.ROUTES:
        return SetData.ROUTES[set_code]
    return get_icon_alias(icon)


"""
* Getting Set and Icon Data
"""


@cache
def get_all_sets() -> list[SetDetails]:
    """Make a GET request to the https://api.scryfall.com/sets endpoint.

    Returns:
        A dictionary of sets where key is set code, value is SetDetails.
    """
    return [
        SetDetails(
            code=n.code,
            type=n.set_type,
            parent=n.parent_set_code.lower() if n.parent_set_code else None,
            icon=get_set_icon(
                set_code=n.code,
                icon=Scryfall.get_icon_code(
                    url=n.icon_svg_uri)),
            name=n.name
        ) for n in Scryfall.get_set_list()
    ]


@cache
def get_all_icons() -> list[Icon]:
    """Returns a (non-repeating) list of all icons found on Scryfall."""
    return [
        Icon.build(icon=k, set_code=v) for k, v in {
            n.icon.upper(): n.code.upper() for n in get_all_sets()
        }.items()
    ]


@cache
def get_all_icon_codes() -> list[str]:
    """Returns a list of all known icon codes."""
    return [n.icon for n in get_all_icons()]


"""
* Icon Checks
"""


def check_icon_recognized(icon: str) -> bool:
    """Check if an icon code is recognized.

    Args:
        icon: Icon code to look for.

    Returns:
        True if icon is recognized, otherwise False.
    """
    return bool(icon in get_all_icon_codes())


def get_unused_icons() -> list[str]:
    """Get a list of icons in the repository not used by any known Scryfall set."""
    return list(
        n for n in os.listdir(Paths.SET)
        if n not in get_all_icon_codes()
        and n not in SetData.IGNORED
    )


def get_missing_icons() -> list[Icon]:
    """Returns a list of Icon objects not found in the repository catalog."""
    return Icon.get_missing(
        items=get_all_icons())


def get_missing_rarities() -> list[Icon]:
    """Returns a list of Icon objects which are missing one or more required rarities."""
    return Icon.get_missing_rarities(
        items=get_all_icons())
