"""
* Commands: Build Scripts
"""
# Standard Library Imports
import os
from pathlib import Path
from time import perf_counter
from typing import Optional

# Third Party Imports
import click
from hexproof.providers.vectors import RarityNameMap
from hexproof.providers.scryfall import ScryURL
from omnitils.files import dump_data_file
from omnitils.logs import logger

# Local Imports
from src.constants import Constants, Paths, SetData, URI
from src.icons import get_missing_icons, get_missing_rarities
from src.watermarks import get_missing_watermarks, get_local_watermarks
from src.schema import Manifest, ManifestMeta, ManifestWatermark, ManifestSet
from src.utils import create_zip, run_inkscape_batch, gather_svg_jobs, get_npm_command, run_svgo_batch

"""
* Commands
"""


@click.command(
    help='Build a `MISSING.md` markdown file which tracks all vector assets currently '
         'missing from the catalogue, based on current scryfall data.')
def build_docs() -> None:
    """Generates the 'MISSING.md' file used in this repository."""
    icons = get_missing_icons()
    rarities = get_missing_rarities()
    missing_wm = get_missing_watermarks()

    # Add to MD file
    with open(Paths.DOCS_MISSING, 'w', encoding='utf-8') as file:

        # Write the list of missing Set Symbols
        file.write('# Missing Set Symbols\n')
        file.write('| Symbol Code | Links |\n')
        file.write('| ----------- | ----- |\n')
        for sym in icons:
            file.write(f'| {sym.icon} | [SVG]({sym.svg_url}), [Cards]({sym.set_url}) |\n')

        # Write the list of missing watermarks
        file.write('\n# Missing Watermarks\n')
        file.write('| Symbol Name | Links |\n')
        file.write('| ----------- | ----- |\n')
        for wm in missing_wm:
            # Format URL queries
            url = ScryURL.API_CARDS_SEARCH.with_query({'q': f'watermark:{wm.lower()}'})
            file.write(f'| {wm.title()} | [Cards]({str(url)}) |\n')

        # Write the list of missing rarities
        file.write('\n# Missing Set Symbol Rarities\n')
        file.write('| Symbol Name | Rarities Missing | Links |\n')
        file.write('| ----------- | ---------------- | ----- |\n')
        for sym in rarities:
            file.write(f'| {sym.icon.upper()} | {sym.missing_str} | '
                       f'[SVG]({sym.svg_url}), [Cards]({sym.set_url}) |\n')

    # Log success
    logger.success('Built ~/docs/MISSING.md file!')


@click.command(
    help='Build a project manifest and compiled package that can be pulled from outside apps.')
def build_manifest() -> None:
    """Generates a manifest of all symbols in the repository and compiles all symbols into
        a zip that can be pulled from outside apps."""
    all_rarities = {str(v): k for k, v in RarityNameMap.items()}

    # Determine the supported symbol rarities
    sym_rarities: dict[str, list[str]] = {}
    for folder in [n for n in os.listdir(Paths.SET) if n not in SetData.IGNORED]:

        # Add rarities for this symbol
        _path = Path(Paths.SET, folder)
        _rarities = set(Path(_path, n).stem.upper() for n in os.listdir(_path))
        sym_rarities[folder] = sorted(n for n in _rarities if n in all_rarities)

    # Generate manifest data
    manifest: Manifest = Manifest(
        meta=ManifestMeta(
            date=Constants.DATE_NOW,
            version=Constants.VERSION_FULL,
            uri=URI.RELEASES
        ),
        set=ManifestSet(
            aliases=SetData.ALIAS.copy(),
            routes=SetData.ROUTES.copy(),
            rarities=all_rarities,
            symbols=dict(sorted(sym_rarities.items()))
        ),
        watermark=ManifestWatermark(
            routes={},
            symbols=sorted(get_local_watermarks())
        )
    )

    # Dump manifest data
    dump_data_file(manifest.model_dump(), Paths.MANIFEST, config={'sort_keys': False})

    # Create packages
    create_zip(
        src=Paths.SVG,
        dst=Paths.PACKAGE_ALL,
        files=[Paths.MANIFEST])
    create_zip(
        src=Paths.SVG_OPTIMIZED,
        dst=Paths.PACKAGE_OPTIMIZED,
        files=[Paths.MANIFEST])

    # Log success
    logger.success('Built manifest and package!')


@click.command(help='Build optimized SVG catalog.')
@click.argument('npm_command', required=False, default=None)
def build_optimized(npm_command: Optional[str] = None) -> None:
    """Generate optimized SVG directories."""

    # Get npm command if not provided
    npm_command = npm_command or get_npm_command()

    # Gather optimization jobs
    dirs = [
        (Paths.SET, Paths.SET_OPTIMIZED),
        (Paths.WATERMARK, Paths.WATERMARK_OPTIMIZED)
    ]

    # Pre-process SVGs with SVGO
    logger.info('Processing: SVGO Normalization ...')
    start = perf_counter()
    _ = [run_svgo_batch(src=x, dst=y, npm_command=npm_command) for x, y in dirs],
    logger.success(f'Completed in {perf_counter() - start:.2f} seconds!')

    # Run Inkscape commands
    files: list[Path] = []
    [files.extend(gather_svg_jobs(n)) for _, n in dirs]
    logger.info('Processing: Inkscape Normalization ...')
    start = perf_counter()
    run_inkscape_batch(files)
    logger.success(f'Completed in {perf_counter() - start:.2f} seconds!')

    # Add final post-process step with SVGO
    logger.info('Processing: SVGO Optimization ...')
    start = perf_counter()
    _ = [run_svgo_batch(src=n, dst=n, npm_command=npm_command) for _, n in dirs],
    logger.success(f'Completed in {perf_counter() - start:.2f} seconds!')
    logger.success('All SVG jobs complete!')


@click.command(
    help='Build docs, manifest, and any other relevant resources used by the repository.')
@click.pass_context
def build_all(ctx: click.Context) -> None:
    """Generate all resources used by the repository."""
    ctx.invoke(build_optimized)
    ctx.invoke(build_manifest)
    ctx.invoke(build_docs)


"""
* Command Groups
"""


@click.group(
    chain=True,
    commands={
        '.': build_all,
        'docs': build_docs,
        'manifest': build_manifest,
        'optimized': build_optimized,
    },
    help='Commands that build repository assets.')
def build_cli():
    """Cli interface for build funcs."""
    pass
