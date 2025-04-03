import typer
from tolvera_sketch.cli import app as sketchbook

app = typer.Typer()


@app.command()
def tolvera_sketch():
    """Entry point for tolvera_sketch."""
    pass

app.add_typer(sketchbook)

if __name__ == "__main__":
    app()
