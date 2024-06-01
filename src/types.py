"""
* Type Definitions Module
"""
# Standard Library Imports
from typing import Optional
from typing_extensions import TypedDict


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
* Types: Manifest
"""


class ManifestMeta(TypedDict):
    """Manifest metadata."""
    date: str
    version: str
    uri: str


class ManifestSet(TypedDict):
    """Set Manifest dict."""
    routes: dict[str, str]
    rarities: dict[str, str]
    symbols: dict[str, list[str]]


class ManifestWatermark(TypedDict):
    """Watermark Manifest dict."""
    routes: dict[str, str]
    symbols: list[str]


class Manifest(TypedDict):
    """Full Manifest dict."""
    meta: ManifestMeta
    set: ManifestSet
    watermark: ManifestWatermark
