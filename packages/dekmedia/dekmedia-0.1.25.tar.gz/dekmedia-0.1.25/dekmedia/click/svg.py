import os
import typer
from typing_extensions import Annotated
from dektools.file import normal_path

app = typer.Typer(add_completion=False)


@app.command()
def design(src, dest: Annotated[str, typer.Argument()] = ""):
    from ..image.svg.design import Manager
    manager = Manager()
    src = normal_path(src)
    if os.path.isfile(src):
        src = os.path.dirname(src)
    manager.load_path(src)
    manager.dump(dest or src)


@app.callback()
def callback():
    pass
