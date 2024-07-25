"""
* Utility Functions
"""
# Standard Library Imports
import os
import shlex
import subprocess
import zipfile
from contextlib import suppress
from pathlib import Path

# Third Party Imports
from omnitils.logs import logger

# Inkscape optimization actions
INKSCAPE_ACTIONS = ';'.join([
    'export-type: svg',
    'export-plain-svg',
    'export-area-drawing',
    'export-do'
])

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


"""
* SVG Utilities
"""


def gather_svg_jobs(src: Path) -> list[Path]:
    """Creates a list of SVG optimization jobs to be processed.

    Args:
        src: Path to the directory containing SVGs to be optimized.

    Returns:
        A list of SVG optimization jobs to be processed, each represented by a tuple
            containing a path to the SVG file and a path the optimized file should be
            created once processed.
    """
    svg_jobs: list[Path] = []
    for node in src.iterdir():
        if node.is_dir():
            # Crawl this directory
            svg_jobs.extend(
                gather_svg_jobs(node))
        elif node.suffix.lower() == '.svg':
            # Add SVG to jobs
            svg_jobs.append(node)
    return svg_jobs


def run_svgo_batch(
    src: Path,
    dst: Path,
    npm_command: str = 'npx.cmd',
    svgo_config: str = 'default.mini.js',
    allow_output: bool = False
) -> None:
    """Run an SVGO batch processing command on a source directory, outputting optimized
        SVG files to the destination directory.

    Args:
        src: Source directory containing SVG files to optimize.
        dst: Path to save optimized SVG files to.
        npm_command: Command to use for running SVGO node module.
        svgo_config: SVGO configuration filename to use.
        allow_output: Whether to allow output from SVGO.
    """

    # Prepare args
    kwargs = {} if allow_output else {'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}

    # Run command
    try:
        subprocess.run([
            npm_command, 'svgo',
            f'--config=svgo/{svgo_config}',
            '-r', '-f', str(src), '-o', str(dst)
        ], **kwargs, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'SVGO batch processing failed!')
        logger.error(f'Reason: {str(e)}')


def run_svgo_optimization(
    src: Path,
    dst: Path,
    npm_command: str = 'npx.cmd',
    svgo_config: str = 'default.mini.js',
    allow_output: bool = False
) -> Path:
    """Run an SVGO command to optimize a target SVG file.

    Args:
        src: Source SVG file to optimize.
        dst: Path to save the optimized SVG file.
        npm_command: Command to use for running SVGO node module.
        svgo_config: SVGO configuration filename to use.
        allow_output: Whether to allow output from SVGO.

    Returns:
        Path to the optimized SVG file.
    """

    # Prepare args
    kwargs = {} if allow_output else {'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}
    command_args = [
        npm_command, 'svgo',
        f'--config=svgo/{svgo_config}',
        '-i', str(src), '-o', str(dst)
    ]

    # Ensure proper escaping
    if os.name == 'nt':
        # Windows
        command_str = subprocess.list2cmdline(command_args)
    else:
        # Unix-like
        command_str = ' '.join(shlex.quote(arg) for arg in command_args)

    # Run command
    try:
        subprocess.run(command_str, **kwargs, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'SVGO failed to process: {str(src)}')
        logger.error(f'Reason: {str(e)}')
    return dst


def run_inkscape_optimization(src: Path, dst: Path, allow_output: bool = False) -> Path:
    """Run an inkscape command to optimize a target SVG file.

    Args:
        src: Source SVG file to optimize.
        dst: Path to save the optimized SVG file.
        allow_output: Whether to allow output from Inkscape.

    Returns:
        Path to the optimized SVG file.
    """

    # Prepare args
    kwargs = {} if allow_output else {'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}
    command_args = [
        'inkscape', '--without-gui',
        f'--actions="{INKSCAPE_ACTIONS}"',
        str(src), '-o', str(dst)
    ]

    # Ensure proper escaping
    if os.name == 'nt':
        # Windows
        command_str = subprocess.list2cmdline(command_args)
    else:
        # Unix-like
        command_str = ' '.join(shlex.quote(arg) for arg in command_args)

    # Run command
    try:
        subprocess.run(command_str, **kwargs, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'Inkscape failed to process: {str(src)}')
        logger.error(f'Reason: {str(e)}')
        input('waiting')
    return dst


def run_inkscape_batch(files: list[Path], allow_output: bool = False) -> None:
    """Run Inkscape batch optimization on a list of SVG files.

    Args:
        files: A list of SVG files to optimize.
        allow_output: Whether to allow output from Inkscape.
    """
    # Prepare args
    _path = os.path.join(os.getcwd(), 'inkscape-commands.txt')
    kwargs = {} if allow_output else {'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}

    # Write commands to file
    with open(_path, 'w', encoding='utf-8') as f:
        for n in files:
            f.write(
                f"file-open:{str(n)}; export-type: svg; export-plain-svg;  "
                f"export-area-drawing; export-filename:{str(n)}; export-do; file-close\n")

    # Run batch commands
    try:
        subprocess.run(
            'inkscape --without-gui --shell < inkscape-commands.txt',
            **kwargs, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'Inkscape encountered an error during batch processing!')
        logger.error(f'Reason: {str(e)}')
    os.remove(_path)


def get_npm_command() -> str:
    """Get the correct command for executing node modules from subprocess."""
    kwargs = dict(
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

    # Try SVGO itself
    with suppress(Exception):
        subprocess.run(['svgo', '--version'], **kwargs)
        return 'svgo'

    # Try running from a node manager
    for command in ['npx', 'npx.cmd', 'pnpm']:
        with suppress(Exception):
            subprocess.run([command, 'svgo', '--version'], **kwargs)
            return command

    # SVGO couldn't be executed
    raise OSError('SVGO does not seem to be installed!')
