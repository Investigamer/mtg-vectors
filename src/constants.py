"""
* App Constants
"""
# Standard Library Imports
from datetime import datetime, date
from pathlib import Path

# Third Party Utils
from omnitils.files import load_data_file

"""
* Global Constant Objects
"""


class Paths:
    """Global project paths."""
    ROOT: Path = Path(__file__).parent.parent
    DATA: Path = ROOT / 'data'

    # SVG Assets
    SVG: Path = ROOT / 'svg'
    SET: Path = SVG / 'set'
    WATERMARK: Path = SVG / 'watermark'
    SVG_OPTIMIZED: Path = SVG / 'optimized'
    SET_OPTIMIZED: Path = SVG_OPTIMIZED / 'set'
    WATERMARK_OPTIMIZED: Path = SVG_OPTIMIZED / 'watermark'

    # Project files
    PACKAGE_ALL: Path = ROOT / 'mtg-vectors.all.zip'
    PACKAGE_OPTIMIZED: Path = ROOT / 'mtg-vectors.optimized.zip'
    CONFIG: Path = ROOT / 'pyproject.toml'
    MANIFEST: Path = ROOT / 'manifest.json'

    # Markdown docs
    DOCS = ROOT / 'docs'
    DOCS_MISSING = DOCS / 'MISSING.md'


class URI:
    """Live hosted resource URLs."""
    RELEASES: str = 'https://api.github.com/repos/Investigamer/mtg-vectors/releases/latest'


class Constants:
    """Global project details."""
    DATE: date = datetime.now()
    DATE_NOW: str = DATE.strftime('%Y-%m-%d')
    CONFIG: dict = load_data_file(Paths.CONFIG)
    VERSION: str = CONFIG.get('tool', {}).get('poetry', {}).get('version', '1.0.0')
    VERSION_FULL: str = f'{VERSION}+{DATE.strftime("%Y%m%d")}'


"""
* Path Constants
"""


class SetPath:
    """Define paths for 'Set' symbol data files."""
    ALIAS: Path = Paths.DATA / 'set' / 'alias.yml'
    EMPTY: Path = Paths.DATA / 'set' / 'empty.yml'
    IGNORED: Path = Paths.DATA / 'set' / 'ignored.yml'
    MIXED: Path = Paths.DATA / 'set' / 'mixed.yml'
    ROUTES: Path = Paths.DATA / 'set' / 'routes.yml'


class WMPath:
    """Define paths for 'Watermark' symbol data files."""
    IGNORED: Path = Paths.DATA / 'watermark' / 'ignored.yml'
    MIXED: Path = Paths.DATA / 'watermark' / 'mixed.yml'


"""
* Data Constants
"""


class SetData:
    """Loaded data for 'Set' symbols."""
    ALIAS: dict[str, str] = load_data_file(SetPath.ALIAS)
    EMPTY: list[str] = load_data_file(SetPath.EMPTY).get('empty', [])
    IGNORED: list[str] = load_data_file(SetPath.IGNORED).get('ignored', [])
    MIXED: list[str] = load_data_file(SetPath.MIXED).get('mixed', [])
    ROUTES: dict[str, str] = dict(sorted(load_data_file(SetPath.ROUTES).items()))


class WMData:
    """Loaded data for 'Watermark' symbols."""
    IGNORED: list[str] = load_data_file(WMPath.IGNORED).get('ignored', [])
    MIXED: list[str] = load_data_file(WMPath.MIXED).get('mixed', [])
