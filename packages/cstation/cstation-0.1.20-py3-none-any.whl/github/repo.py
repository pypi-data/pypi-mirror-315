import typer
import os

from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def sync(
    config: Annotated[
        typer.FileText, typer.Option()
    ] = "/opt/cstation/etc/github_repo.yaml",
):
    """
        Sync the Github repositories with the upstream repositories
    """
    for line in config:
        if line.strip() != "" or line.startswith('#'):
            print(f"gh repo sync {line.strip()}")
            os.system(f"gh repo sync {line.strip()}")

if __name__ == "__main__":
    app()
