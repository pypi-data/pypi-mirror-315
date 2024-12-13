import typer
from dektools.shell import associate_console_script

app = typer.Typer(add_completion=False)


@app.command()
def assoc():
    associate_console_script('.designignore', __name__, 'Design', 'image design')
    associate_console_script('.svgdesignignore', __name__, 'SvgDesign', 'image svg design')
