"""
* MTG Vectors
* Data Gathering and Test Commands
"""
# Third Party Imports
import click

# Local Imports
from src.commands.build import build_cli, build_all
from src.commands.test import test_cli

"""
* App CLI
"""


@click.group(
    commands={
        'build': build_cli,
        'test': test_cli
    },
    help='Invoke the CLI without a command to launch an ongoing headless Proxyshop application.')
def AppCLI():
    pass


# Export CLI
__all__ = ['AppCLI']
