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
    SET: Path = ROOT / 'svg' / 'set'
    DATA: Path = ROOT / 'data'
    PKG: Path = ROOT / 'package'
    CONFIG: Path = ROOT / 'pyproject.toml'


class URI:
    """Live hosted resource URLs."""
    PKG_SET: str = 'https://raw.githubusercontent.com/Investigamer/mtg-vectors/main/package/set.zip'


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
    MANIFEST: Path = Paths.DATA / 'manifest.set.json'


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
