import typer
from datetime import datetime
from pathlib import Path
from typing import Optional
import os

app = typer.Typer()


@app.command()
def init(
    name: str = typer.Argument(..., help="Name of the sketchbook folder"),
    path: Optional[Path] = typer.Option(
        None, "--path", "-p", help="Path where sketchbook will be created [Optional]"
    ),
    template: bool = typer.Option(
        True,
        "--template",
        "-t",
        help="Create sketchbook with template files (default: True)",
    ),
):
    """
    Create a new sketchbook folder with optional templates.
    """

    # if path is not given use current working directory
    if path is None:
        path = Path.cwd()

    sketchbook_path = path / name

    try:
        sketchbook_path.mkdir(parents=True, exist_ok=False)
        typer.echo(f"Created {name} at: {sketchbook_path}")

        if template:
            (sketchbook_path / "sketches").mkdir()
            (sketchbook_path / "README.md").touch()
            (sketchbook_path / "pyproject.toml").touch()

            pyproject_path = sketchbook_path / "pyproject.toml"
            with open(pyproject_path, "w") as f:
                f.write(
f"""[tool.poetry]
name = "{name.lower().replace(' ', '-')}"
version = "0.1.0"
description = "A tolvera sketchbook"
readme = "README.md"
packages = []

[tool.poetry.dependencies]
python = "^3.11"

[tool.poetry.dev-dependencies]
black = "^23.3.0"
isort = "^5.12.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

"""
)

            readme_path = sketchbook_path / "README.md"
            with open(readme_path, "w") as f:
                f.write(f"# {name} Sketchbook\n")
                f.write(f"Created on: {datetime.now().strftime('%Y-%m-%d')}\n")
                f.write("## Structure\n")
                f.write(
                    "- **sketches/**: Directory to store all your sketches within a sketchbook\n"
                )
                f.write("- **main.py**: Entry point for the sketchbook\n")
                f.write("- **pyproject.toml**: Manages dependencies among sketches\n")

            main_py_path = sketchbook_path / "main.py"
            with open(main_py_path, "w") as f:
                f.write(
                    """import os
import subprocess

SKETCH_DIR = "sketches"

def list_sketches():
    return [f for f in os.listdir(SKETCH_DIR) if f.endswith(".py")]

if __name__ == "__main__":
    sketches = list_sketches()
    if not sketches:
        print("No sketches found in the 'sketches/' folder.")
    else:
        print("Available Sketches:")
        for idx, sketch in enumerate(sketches, 1):
            print(f"{idx}. {sketch}")
        
        choice = input("Enter the sketch number to run: ")
        try:
            sketch_file = sketches[int(choice) - 1]
            sketch_path = os.path.join(SKETCH_DIR, sketch_file)
            subprocess.run(["python", sketch_path], check=True)
        except (IndexError, ValueError):
            print("Invalid input. Exiting.")
        except subprocess.CalledProcessError as e:
            print(f"Error running {sketch_file}: {e}")

"""
                )

            typer.echo(
                "Created template structure with sketches, pyproject.toml, README, and main.py"
            )

    except FileExistsError:
        typer.echo(f"Error: Sketchbook '{name}' already exists at {path}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error creating sketchbook: {str(e)}", err=True)
        raise typer.Exit(code=1)


SKETCH_DIR_NAME = "sketches"


@app.command()
def list_sketches(sketchbook_path):
    """List all Python sketches in the sketches folder, sorted by name."""
    sketches_path = os.path.join(sketchbook_path, SKETCH_DIR_NAME)
    print(sketches_path)
    if not os.path.exists(sketches_path):
        return []
    typer.echo(sorted([f for f in os.listdir(sketches_path) if f.endswith(".py")]))


if __name__ == "__main__":
    app()
