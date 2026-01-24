"""
* Commands: Scryfall Data
"""
# Standard Library Imports
from typing import Optional

# Third Party Imports
import click
from hexproof.providers.scryfall import ScryURL
from omnitils.logs import logger

# Local Imports
from src.constants import SetData
from src.icons import get_all_sets, get_missing_rarities, get_missing_icons
from src.watermarks import get_missing_watermarks
from src.schema import SetDetails

"""
* Commands
"""


@click.command(
    help='Lists all sets that match a provided query.')
@click.option(
    '-i', '--icon',
    required=False, default=None,
    help='Match a provided Scryfall icon name.')
def list_sets_by_symbol(icon: Optional[str] = None) -> None:
    """Print a list of Scryfall sets that use a given SVG symbol.

    Args:
        icon: The name of an SVG icon recognized by Scryfall.
    """
    for n in get_all_sets():
        # Check symbol match
        if icon is None or icon.lower() in n.icon.lower():
            logger.info(
                f"[{n.code.upper():<5}| {n.icon}.svg] {n.name} "
                f"{'' if not n.parent else f'(Parent: {n.parent.upper()})'} "
                f"<{n.type}>")


"""
* Test Missing Assets
"""


@click.command(
    help="Lists all sets that currently don't have a matching vector symbol catalogued in this repository.")
def list_missing_icons() -> None:
    """List any sets that don't have a matching vector symbol found in this repository."""

    # Check for missing icons
    if icons := get_missing_icons():
        logger.info('The following icons are missing from the catalog:')
        [logger.warning(f'{n.icon} ({n.set_code}) {n.svg_url}') for n in icons]
    else:
        logger.success('All icons exist in the catalog!')

    # Check for missing rarities
    if rarities := get_missing_rarities():
        logger.info('The following icons have missing rarity treatments:')
        [logger.warning(f'{n.icon} | {n.missing_str} | {n.svg_url})') for n in rarities]
    else:
        logger.success('All rarities for catalogued icons are accounted for!')


@click.command(
    help="Lists all watermark names that don't have matching vector symbol catalogued in this repository.")
def list_missing_watermarks() -> None:
    """List any watermarks that don't have a matching vector symbol found in this repository."""

    # Check for missing watermarks
    if watermarks := get_missing_watermarks():
        logger.info('The following watermarks are missing from the catalog:')
        for wm in watermarks:
            url = ScryURL.API_CARDS_SEARCH.with_query(
                {'q': f'watermark:{wm.lower()}'})
            logger.warning(f"{wm} | {str(url)}")
    else:
        logger.success('All watermarks exist in the catalog!')


@click.command(help='List all SVG assets that are missing from the repository.')
@click.pass_context
def list_missing_all(ctx: click.Context) -> None:
    """List all SVG assets (set, watermarks, etc) that are present in Scryfall data but missing from
        this repository.
    """
    ctx.invoke(list_missing_icons)
    ctx.invoke(list_missing_watermarks)


"""
* Test Data Files
"""


@click.command
def test_routes():
    """Checks defined routes."""
    sets: dict[str, SetDetails] = get_all_sets()
    missing = []
    for set_code, icon_code in SetData.ROUTES.items():
        _set = sets.get(set_code.lower())
        if _set is None:
            missing.append(f'[MISSING] {set_code} (Not found in Scryfall data)')
            continue
        _icon = _set.icon
        if icon_code.upper() != _icon:
            logger.info(f'[ROUTED] {set_code}: {icon_code} (From: {_icon})')
            continue
        # Code matched
        logger.success(f'[NORMAL] {set_code}: {_icon} (Scryfall now matches this route)')
    [logger.error(m) for m in missing]


"""
* Command Groups
"""


@click.group(
    chain=True,
    commands={
        '.': list_missing_all,
        'watermarks': list_missing_watermarks,
        'icons': list_missing_icons
    },
    help='A suite of commands for testing for missing assets in the SVG catalog.'
)
def test_missing_cli():
    """CLI interface for testing for missing SVG assets."""
    pass


@click.group(
    chain=True,
    commands={
        'sets': list_sets_by_symbol
    },
    help='A suite of commands for testing the retrieval of bulk data.'
)
def test_get_cli():
    """CLI interface for returning bulk data."""
    pass


@click.group(
    chain=True,
    commands={
        'missing': test_missing_cli,
        'get': test_get_cli,
        'routes': test_routes
    },
    help='A suite of commands for testing the project and the asset catalog.')
def test_cli():
    """CLI interface for running project tests."""
    pass
