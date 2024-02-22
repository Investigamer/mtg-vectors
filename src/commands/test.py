"""
* Commands: Scryfall Data
"""
from pprint import pprint

# Third Party Imports
import click

# Local Imports
from src.symbols_set import get_all_sets, get_missing_symbols_set
from src.symbols_wm import get_missing_symbols_watermark
from src.types import SetDetails


"""
* Command Groups
"""


@click.group(
    name='test', chain=True,
    help='Commands that run data tests.')
def test_cli():
    """Cli interface for test funcs."""
    pass


"""
* Commands
"""


@test_cli.command(
    name='list-sets-by-symbol',
    help='Lists all sets that use a specific symbol icon.')
@click.argument('sym', required=True)
def list_sets_by_symbol(sym: str) -> dict[str, SetDetails]:
    """Return a list of set codes that use a given SVG symbol.

    Args:
        sym: The name of an SVG set symbol recognized by Scryfall.

    Returns:
        A list of Scryfall 'set' objects that use the given symbol.
    """
    data = {code: v for code, v in get_all_sets().items() if sym.lower() in v['icon']}
    pprint(data)
    return data


@test_cli.command(
    name='list-missing-sets',
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


@test_cli.command(
    name='list-missing-watermarks',
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
