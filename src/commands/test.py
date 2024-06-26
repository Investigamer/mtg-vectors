"""
* Commands: Scryfall Data
"""
from pprint import pprint
from typing import Optional

# Third Party Imports
import click
from loguru import logger

# Local Imports
from src.symbols_set import get_all_sets, get_missing_symbols_set
from src.symbols_wm import get_missing_symbols_watermark
from src.types import SetDetails

"""
* Commands
"""


@click.command(
    help='Lists all sets that match a provided query.')
@click.option(
    '-s', '--sym',
    required=False, type=str, help='Match a provided Scryfall icon (symbol) name.')
def list_sets_by_symbol(sym: Optional[str] = None) -> dict[str, SetDetails]:
    """Return a list of set codes that use a given SVG symbol.

    Args:
        sym: The name of an SVG icon recognized by Scryfall.

    Returns:
        A list of Scryfall 'set' objects that use the given symbol.
    """
    data = {}
    for code, v in get_all_sets().items():
        # Check symbol match
        if sym is None or sym.lower() in v['icon'].lower():
            parent = '' if not v['parent'] else f"(Parent: {v['parent'].upper()})"
            logger.info(f"[{code.upper():<5}| {v['icon']}.svg] {v['name']} {parent} <{v['type']}>")
        data[code] = v
    return data


@click.command(
    help="Lists all sets that currently don't have a matching vector symbol catalogued in this repository.")
def list_missing_symbols_set() -> None:
    """List any sets that don't have a matching vector symbol found in this repository."""

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


@click.command(
    help="Lists all watermark names that don't have matching vector symbol catalogued in this repository.")
def list_missing_symbols_watermark() -> None:
    """List any watermarks that don't have a matching vector symbol found in this repository."""

    # Get any missing sets
    missing = get_missing_symbols_watermark()

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
* Command Groups
"""


@click.group(
    chain=True,
    commands={
        'missing-watermarks': list_missing_symbols_watermark,
        'missing-sets': list_missing_symbols_set,
        'list-sets': list_sets_by_symbol
    },
    help='Commands that run data tests.')
def test_cli():
    """Cli interface for test funcs."""
    pass
