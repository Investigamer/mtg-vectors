import os
import subprocess
from pathlib import Path

import typer

hooks = typer.Typer(add_completion=False, no_args_is_help=True)

"""
* Utils
"""


def run_command(cmd: list[str], *, cwd: Path | None = None) -> None:
    """Run a command and raise a Typer-friendly error if it fails."""
    try:
        proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=False)
    except FileNotFoundError:
        raise typer.Exit(code=127)
    if proc.returncode != 0:
        raise typer.Exit(code=proc.returncode)


def version_context() -> tuple[str | None, str | None]:
    """Retrieve commitizen version context."""
    new_ver = os.getenv("CZ_PRE_NEW_VERSION") or os.getenv("CZ_POST_NEW_VERSION")
    cur_ver = os.getenv("CZ_PRE_CURRENT_VERSION") or os.getenv("CZ_POST_CURRENT_VERSION")
    return cur_ver, new_ver


"""
* Hooks
"""


@hooks.command("pre-bump")
def pre_bump(stage_lockfile: bool = typer.Option(True, "--stage/--no-stage")) -> None:
    """Run before Commitizen creates the bump commit/tag."""
    cur_ver, new_ver = version_context()
    typer.echo(f"[pre-bump] pre-bump ({cur_ver} -> {new_ver})")

    # Generate new lock file
    typer.echo("[pre-bump] running: uv lock")
    run_command(["uv", "lock"])

    # Stage lock file so it is committed to new version
    if stage_lockfile:
        typer.echo("[pre-bump] running: git add uv.lock")
        run_command(["git", "add", "uv.lock"])


@hooks.command("post-bump")
def post_bump() -> None:
    """Run after Commitizen creates the bump commit/tag."""
    typer.echo(f"[post-bump] This hook is not implemented!")


if __name__ == "__main__":
    hooks()
