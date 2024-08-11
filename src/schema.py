"""
* Type Definitions Module
"""
# Standard Library Imports
from pathlib import Path
from typing import Optional

# Third Party Imports
import yarl
from omnitils.schema import Schema

# Local Imports
from src.constants import Paths

# Rarities to test for
REQUIRED_RARITIES: set[str] = {'C', 'U', 'R', 'M', 'T', 'WM'}

"""
* Set Schemas
"""


class SetDetails(Schema):
    """Set details dictionary."""
    type: str
    parent: Optional[str] = None
    icon: str
    name: str
    code: str


"""
* Icon Schemas
"""


class Icon(Schema):
    """An icon missing from the catalog."""
    icon: str
    set_code: str
    path: Path
    set_url: str
    svg_url: str
    exists: bool
    missing: list[str]
    found: list[str]
    missing_str: str | None

    @classmethod
    def build(cls, icon: str = '', set_code: str = '') -> 'Icon':
        """Build and return a new Icon object.

        Args:
            icon: The icon code.
            set_code: The Scryfall recognized set code.

        Returns:
            An Icon object.
        """

        # Build directory path and discover missing rarities
        _path = Path(Paths.SET, icon.upper())
        _missing = [
            n for n in REQUIRED_RARITIES
            if not Path(_path, n).with_suffix('.svg').is_file()
        ]

        # Return generated Icon object
        return Icon(
            icon=icon,
            set_code=set_code,
            path=_path,
            set_url=str(yarl.URL('https://scryfall.com/sets') / set_code.lower()),
            svg_url=str((yarl.URL('https://svgs.scryfall.io/sets') / icon.lower()).with_suffix('.svg')),
            exists=_path.is_dir(),
            missing=_missing,
            found=[n for n in REQUIRED_RARITIES if n not in _missing],
            missing_str=', '.join(_missing) if _missing else None
        )

    @classmethod
    def get_missing(cls, items: list['Icon']) -> list['Icon']:
        """Takes in a list of Icon objects and returns a list of Icon objects which are not found
            in the repository catalog, sorted alphabetically.

        Args:
            items (list[Icon]): A list of Icon objects.

        Returns:
            list[Icon]: A list of Icon objects missing from the repository catalog.
        """
        _items = [n for n in items if not n.exists]
        return sorted(_items, key=lambda n: n.icon)

    @classmethod
    def get_missing_rarities(cls, items: list['Icon']) -> list['Icon']:
        """Takes in a list of Icon objects and returns a list of Icon objects which are missing
            required rarities, sorted primarily by most rarities missing to least, sorted secondarily
            in alphabetical order.

        Args:
            items (list[Icon]): A list of Icon objects.

        Returns:
            list[Icon]: A list of Icon objects missing required rarities.
        """
        # Get items with missing rarities
        _items = [n for n in items if n.exists and n.missing]

        # Sort alphabetically
        _items = sorted(_items, key=lambda n: n.icon)

        # Sort by number if rarities missing
        return sorted(_items, key=lambda n: len(n.missing), reverse=True)


"""
* Manifest Schemas
"""


class ManifestMeta(Schema):
    """Manifest metadata."""
    date: str
    version: str
    uri: str


class ManifestSet(Schema):
    """Set Manifest dict."""
    aliases: dict[str, str]
    routes: dict[str, str]
    rarities: dict[str, str]
    symbols: dict[str, list[str]]


class ManifestWatermark(Schema):
    """Watermark Manifest dict."""
    routes: dict[str, str]
    symbols: list[str]


class Manifest(Schema):
    """Full Manifest dict."""
    meta: ManifestMeta
    set: ManifestSet
    watermark: ManifestWatermark
