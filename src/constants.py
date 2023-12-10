# Base Paths
from datetime import datetime, date
from pathlib import Path

# Third Party Utils
from src.utils import load_data_file

"""
* Global Constant Objects
"""


class Paths:
    """Global project paths."""
    ROOT: Path = Path(__file__).parent.parent
    DATA: Path = ROOT / 'data'

    # SVG Assets
    SVG: Path = ROOT / 'svg'
    SET: Path = ROOT / 'svg' / 'set'
    WATERMARK: Path = ROOT / 'svg' / 'watermark'

    # Project files
    PACKAGE: Path = ROOT / 'package.zip'
    CONFIG: Path = ROOT / 'pyproject.toml'
    MANIFEST: Path = ROOT / 'manifest.json'

    # Markdown files
    MD_MISSING = ROOT / 'MISSING.md'


class URI:
    """Live hosted resource URLs."""
    PACKAGE: str = 'https://raw.githubusercontent.com/Investigamer/mtg-vectors/main/package.zip'


class Constants:
    """Global project details."""
    DATE: date = datetime.now()
    DATE_NOW: str = DATE.strftime('%Y-%m-%d')
    CONFIG: dict = load_data_file(Paths.CONFIG)
    VERSION: str = CONFIG.get('tool', {}).get('poetry', {}).get('version', '1.0.0')
    VERSION_FULL: str = f'{VERSION}+{DATE.strftime("%Y%m%d")}'


"""
* 'Set' Symbol Specific Constants
"""


class SetPath:
    """Define paths for 'Set' symbol data files."""
    ALIAS: Path = Paths.DATA / 'set' / 'alias.yml'
    CORRECTED: Path = Paths.DATA / 'set' / 'corrected.yml'
    EMPTY: Path = Paths.DATA / 'set' / 'empty.yml'
    IGNORED: Path = Paths.DATA / 'set' / 'ignored.yml'
    MISSING: Path = Paths.DATA / 'set' / 'missing.yml'
    MIXED: Path = Paths.DATA / 'set' / 'mixed.yml'
    ROUTES: Path = Paths.DATA / 'set' / 'routes.yml'
    RARITIES: Path = Paths.DATA / 'set' / 'rarities.yml'


class SetData:
    """Loaded data for 'Set' symbols."""
    ALIAS: dict[str, list[str]] = load_data_file(SetPath.ALIAS)
    CORRECTED: dict[str, str] = load_data_file(SetPath.CORRECTED)
    EMPTY: list[str] = load_data_file(SetPath.EMPTY).get('empty', [])
    IGNORED: list[str] = load_data_file(SetPath.IGNORED).get('ignored', [])
    MISSING: dict[str, str] = load_data_file(SetPath.MISSING)
    MIXED: list[str] = load_data_file(SetPath.MIXED).get('mixed', [])
    RARITIES: list[str] = load_data_file(SetPath.RARITIES).get('rarities', [])
    ROUTES: dict[str, str] = dict(sorted(load_data_file(SetPath.ROUTES).items()))


"""Define recognized rarities for set symbols."""
SetRarities = {
    'WM': 'Watermark',
    'C': 'Common',
    'U': 'Uncommon',
    'R': 'Rare',
    'M': 'Mythic',
    'S': 'Special',
    'T': 'Timeshifted',
    'B': 'Bonus',
    '80': '80',
    'H': 'Half'
}
