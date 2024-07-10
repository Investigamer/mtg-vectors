"""
* Utility Functions
"""
# Standard Library Imports
import os
import zipfile
from pathlib import Path

"""
* Archive Utils
"""


def create_zip(src: Path, dst: Path) -> None:
    """Create a `.zip` archive containing the contents of a given source directory.
    Args:
        src: Path to the source directory.
        dst: Path to the destination `.zip` file.
    """
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, src)
                zipf.write(file_path, rel_path)
