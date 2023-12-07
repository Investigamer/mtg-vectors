"""
* Type Definitions Module
"""
# Standard Library Imports
from typing import Optional
from typing_extensions import TypedDict

# Local Imports
from src.constants import URI


"""
* Types: Set Data
"""


class SetDetails(TypedDict):
    """Set details dictionary."""
    type: str
    parent: Optional[str]
    icon: str
    name: str


"""
* Types: Set Symbols
"""


class SetManifestMeta(TypedDict):
    """Set manifest metadata details."""
    date: str
    version: str
    uri: type[URI.PKG_SET]
    routes: dict[str, str]


class SetManifest(TypedDict):
    """Set manifest details."""
    meta: SetManifestMeta
    symbols: dict[str, list[str]]
