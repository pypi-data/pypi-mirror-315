from wiever.core.viewer.ascii_tree import AsciiTree

import typer
from typing_extensions import Annotated
from typing import List

app = typer.Typer(help="Display directory structure in ASCII format.")

@app.command()
def ascii(
        root_dir: Annotated[str, typer.Argument(help="The root directory to display the tree for.")] = ".", 
        depth: Annotated[int, typer.Option(min = 0, help="Maximum depth to traverse. Default is 0 (no limit).")] = 0,
        exclude: Annotated[List[str], typer.Option("--exclude", "-e", help="Exclude files or directories.")] = None,
        include: Annotated[List[str], typer.Option("--include", "-i", help="Include only files or directories.")] = None,
        pattern: Annotated[str, typer.Option("--pattern" , "-p" , help="Pattern to match files or directories.")] = None
    ):
    tree = AsciiTree(root_dir=root_dir, max_depth=depth, include=include, exclude=exclude, regex=pattern)
    tree.display()
