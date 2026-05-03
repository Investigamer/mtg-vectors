"""
* Commands: Scryfall Data
"""
# Third Party Imports
import typer
from hexproof.providers.scryfall import ScryURL
from omnitils.logs import logger

# Local Imports
from src.constants import SetData
from src.icons import get_all_sets_raw, get_missing_rarities, get_missing_icons
from src.watermarks import get_missing_watermarks
from src.schema import SetDetails

# Typer group
app = typer.Typer(
    name="test",
    help="A suite of commands for testing the project and the asset catalog."
)

"""
* Commands
"""


@app.command(
    "sets",
    help='Lists all sets that match a provided query.'
)
def list_sets_by_query(
        icon: str | None = typer.Option(
            None, '-i', "--icon",
            help='Match a provided Scryfall icon name.'
        )
) -> None:
    """Print a list of Scryfall sets that match a variety of options.

    Todo:
        Add more options.

    Args:
        icon: The name of an SVG icon recognized by Scryfall.
    """
    for n in get_all_sets_raw():
        # Check symbol match
        if icon is None or icon.lower() in n.icon.lower():
            logger.info(
                f"[{n.code.upper():<5}| {n.icon}.svg] {n.name} "
                f"{'' if not n.parent else f'(Parent: {n.parent.upper()})'} "
                f"[{n.type}]")


"""
* Test Missing Assets
"""


@app.command(
    "icons",
    help="Lists all sets that currently don't have a matching vector symbol catalogued in this repository."
)
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


@app.command(
    "wm",
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


@app.command(
    "missing",
    help='List all SVG assets that are missing from the repository.'
)
def list_missing_all(ctx: typer.Context) -> None:
    """List all SVG assets (set, watermarks, etc) that are present in Scryfall data but missing from
        this repository.
    """
    ctx.invoke(list_missing_icons)
    ctx.invoke(list_missing_watermarks)


@app.command(
    "routes",
    help="Lists all sets that don't have a matching vector symbol catalogued in this repository."
)
def test_routes():
    """Checks defined routes."""
    sets: list[SetDetails] = get_all_sets_raw()
    set_map = {n.code.lower(): n for n in sets}
    missing = []
    for set_code, icon_code in SetData.ROUTES.items():
        _set = set_map.get(set_code.lower())
        if _set is None:
            missing.append(f'[MISSING] {set_code} (Not found in Scryfall data)')
            continue
        _icon = _set.icon.upper()
        if icon_code.upper() != _icon:
            logger.info(f'[ROUTED] {set_code}: {icon_code} (From: {_icon})')
            continue
        # Code matched
        logger.success(f'[NORMAL] {set_code}: {_icon} (Scryfall now matches this route)')
    [logger.error(m) for m in missing]
