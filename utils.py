"""
* Utility Functions
"""
# Standard Library Imports
import os
import json
from pathlib import Path
from typing import Optional, TypedDict, Callable, Union
from threading import Lock

# Third Party Imports
from yaml import (
    load as yaml_load,
    dump as yaml_dump,
    Loader as yamlLoader,
    Dumper as yamlDumper)
from tomlkit import dump as toml_dump, load as toml_load

"""
* Types
"""


class DataFileType (TypedDict):
    """Data file type (json, toml, yaml, etc)."""
    load: Callable
    dump: Callable
    load_kw: dict[str, Union[Callable, bool, str]]
    dump_kw: dict[str, Union[Callable, bool, str]]


"""
* Constants
"""

# File util locking mechanism
util_file_lock = Lock()

# Data types for loading test case files
data_types: dict[str, DataFileType] = {
    'toml': {
        'load': toml_load, 'load_kw': {},
        'dump': toml_dump, 'dump_kw': {'sort_keys': True}
    },
    'yml': {
        'load': yaml_load, 'load_kw': {'Loader': yamlLoader},
        'dump': yaml_dump, 'dump_kw': {
            'Dumper': yamlDumper,
            'sort_keys': True,
            'indent': 2,
            'allow_unicode': True}
    },
    'yaml': {
        'load': yaml_load, 'load_kw': {'Loader': yamlLoader},
        'dump': yaml_dump, 'dump_kw': {
            'Dumper': yamlDumper,
            'sort_keys': True,
            'indent': 2,
            'allow_unicode': True}
    },
    'json': {
        'load': json.load, 'load_kw': {},
        'dump': json.dump, 'dump_kw': {
            'sort_keys': True,
            'indent': 2,
            'ensure_ascii': False
        }
    }
}


"""
* File Info Utils
"""


def get_file_size_mb(file_path: Union[str, os.PathLike], decimal: int = 1) -> float:
    """
    Get a file's size in megabytes rounded.
    @param file_path: Path to the file.
    @param decimal: Number of decimal places to allow when rounding.
    @return: Float representing the filesize in megabytes rounded.
    """
    return round(os.path.getsize(file_path) / (1024 * 1024), decimal)


"""
* Data File Utils
"""


def load_data_file(
    data_file: Union[str, os.PathLike],
    config: Optional[dict] = None
) -> Union[list, dict, tuple, set]:
    """
    Load object from a data file.
    @param data_file: Path to the data file to be loaded.
    @param config: Dict data to modify DataFileType configuration for this data load procedure.
    @return: Iterable or dict object loaded from data file.
    @raise ValueError: If data file type not supported.
    @raise OSError: If loading data file fails.
    """
    data_type = Path(data_file).suffix[1:]
    parser: DataFileType = data_types.get(data_type, {}).copy()
    if not parser:
        raise ValueError("Data file provided does not match a supported data file type.\n"
                         f"Types supported: {', '.join(data_types.keys())}\n"
                         f"Type received: {data_type}")
    if config:
        parser['load_kw'].update(config)
    with util_file_lock:
        with open(data_file, 'r', encoding='utf-8') as f:
            try:
                return parser['load'](f, **parser['load_kw']) or {}
            except Exception as e:
                raise OSError(f"Unable to load data from data file:\n{data_file}") from e


def dump_data_file(
    obj: Union[list, dict, tuple, set],
    data_file: Union[str, os.PathLike],
    config: Optional[dict] = None
) -> None:
    """
    Dump object to a data file.
    @param obj: Iterable or dict object to save to data file.
    @param data_file: Path to the data file to be dumps.
    @param config: Dict data to modify DataFileType configuration for this data dump procedure.
    @raise ValueError: If data file type not supported.
    @raise OSError: If dumping to data file fails.
    """
    data_type = Path(data_file).suffix[1:]
    parser: DataFileType = data_types.get(data_type, {})
    if not parser:
        raise ValueError("Data file provided does not match a supported data file type.\n"
                         f"Types supported: {', '.join(data_types.keys())}\n"
                         f"Type received: {data_type}")
    if config:
        parser['dump_kw'].update(config)
    with util_file_lock:
        with open(data_file, 'w', encoding='utf-8') as f:
            try:
                parser['dump'](obj, f, **parser['dump_kw'])
            except Exception as e:
                raise OSError(f"Unable to dump data to data file:\n{data_file}") from e
