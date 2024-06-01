"""
* Commands: Build Scripts
"""
import os
from pathlib import Path

# Third Party Imports
import click
import yarl
from omnitils.files import dump_data_file

# Local Imports
from src.constants import Constants, Paths, SetData, SetRarities, URI
from src.symbols_set import get_missing_symbols_set, get_missing_symbols_set_rarities
from src.symbols_wm import get_missing_symbols_watermark, get_local_watermarks
from src.types import Manifest
from src.utils import create_zip

"""
* Command Groups
"""


@click.group(
    name='build', chain=True,
    help='Commands that build repository assets.')
def build_cli():
    """Cli interface for build funcs."""
    pass


"""
* Commands
"""


@build_cli.command(
    name='docs',
    help='Builds the MISSING.md file which tracks all vector assets currently missing from the catalogue.')
def build_docs() -> None:
    """Generates the 'MISSING.md' file used in this repository."""
    missing_set = [(k.upper(), v[0].lower()) for k, v in get_missing_symbols_set().items()]
    missing_rarities = get_missing_symbols_set_rarities()
    missing_wm = get_missing_symbols_watermark()

    # Add to MD file
    with open(Paths.DOCS_MISSING, 'w', encoding='utf-8') as file:
        file.write('# Missing Set Symbols\n')
        file.write('| Symbol Code   | Links         |\n')
        file.write('| ------------- | ------------- |\n')
        for symbol, code in missing_set:
            file.write(f'| {symbol.upper()} |'
                       f'[SVG](https://svgs.scryfall.io/sets/{symbol.lower()}.svg), '
                       f'[Cards](https://scryfall.com/sets/{code.lower()}) |\n')
        file.write('\n# Missing Watermarks\n')
        file.write('| Symbol Name   | Links         |\n')
        file.write('| ------------- | ------------- |\n')
        for wm in missing_wm:
            # Format URL queries
            url = yarl.URL('https://scryfall.com/search').with_query({'q': f'watermark:{wm.lower()}'})
            file.write(f'| {wm.title()} | [Cards]({str(url)}) |\n')
        file.write('\n# Missing Set Symbol Rarities\n')
        file.write('| Symbol Name   | Rarities Missing | Links |\n')
        file.write('| ------------- | ---------------- | ----- |\n')
        for symbol, missing in missing_rarities:
            file.write(f'| {symbol.upper()} '
                       f'| {missing} |'
                       f'[SVG](https://svgs.scryfall.io/sets/{symbol.lower()}.svg), '
                       f'[Cards](https://scryfall.com/sets/{code.lower()}) |\n')


@build_cli.command(name='manifest')
def build_manifest() -> None:
    """Generates a manifest of all symbols in the repository and compiles all symbols into
        a zip that can be pulled from outside apps."""
    manifest: Manifest = {
        'meta': {
            'date': Constants.DATE_NOW,
            'version': Constants.VERSION_FULL,
            'uri': URI.PACKAGE
        },
        'set': {
            'routes': SetData.ROUTES.copy(),
            'rarities': SetRarities.copy(),
            'symbols': {}
        },
        'watermark': {
            'routes': {},
            'symbols': []
        }
    }

    # Determine the supported rarities in each symbol directory
    for folder in os.listdir(Paths.SET):
        # Ignored folders
        if folder in ['.alt', '.extras']:
            continue
        # Add rarities to manifest
        manifest['set']['symbols'][folder] = [
            Path(svg).stem for svg in
            os.listdir(Path(Paths.SET, folder))
            if svg.upper().strip('.svg') not in SetData.RARITIES]

    # Sort Set Symbols
    manifest['set']['symbols'] = dict(sorted(manifest['set']['symbols'].items())).copy()

    # Create a sorted list of watermarks
    manifest['watermark']['symbols'] = sorted(get_local_watermarks())

    # Dump manifest file
    dump_data_file(manifest, Paths.MANIFEST, config={'sort_keys': False})

    # Create a zip of all symbols
    create_zip(Paths.SVG, Paths.PACKAGE)


@build_cli.command(
    name='all',
    help='Build docs, manifest, and any other relevant resources used by the repository.')
@click.pass_context
def build_all(ctx: click.Context) -> None:
    """Generate all resources used by the repository."""
    ctx.invoke(build_manifest)
    ctx.invoke(build_docs)
