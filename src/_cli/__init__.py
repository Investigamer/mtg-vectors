"""
* MTG Vectors
* Data Gathering and Test Commands
"""
# Third Party Imports
import typer

# Local Imports
from src._cli.build import app as app_build
from src._cli.test import app as app_test

"""
* App CLI
"""


app = typer.Typer(
    name="vectors",
    help="Invoke the CLI without a command to launch an ongoing headless Proxyshop application."
)
app.add_typer(app_build)
app.add_typer(app_test)


# Export CLI
__all__ = ['app']
