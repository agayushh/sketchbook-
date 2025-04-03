import typer
from datetime import datetime
from pathlib import Path
from typing import Optional

# Create an app with subcommands
app = typer.Typer()

@app.command()
def init(
    name: str = typer.Argument(..., help="Name of the sketchbook folder"),
    path: Optional[Path] = typer.Option(
        None, "--path", "-p", help="Path where sketchbook should be created"
    ),
    template: bool = typer.Option(
        True, "--template", "-t", help="Create sketchbook with template files (default: True)"
    )
):
    """
    Create a new sketchbook folder with optional templates.
    """
    if path is None:
        path = Path.cwd()
    
    sketchbook_path = path / name
    
    try:
        sketchbook_path.mkdir(parents=True, exist_ok=False)
        typer.echo(f"✅ Created sketchbook folder: {sketchbook_path}")
        
        if template:
            (sketchbook_path / "sketches").mkdir()
            (sketchbook_path / "README.md").touch()

            readme_path = sketchbook_path / "README.md"
            with open(readme_path, "w") as f:
                f.write(f"# {name} Sketchbook\n\n")
                f.write(f"Created on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write("## Structure\n\n")
                f.write("- **sketches/**: Store your sketch files here\n")
                f.write("- **main.py**: Main script to run sketches\n")

            main_py_path = sketchbook_path / "main.py"
            with open(main_py_path, "w") as f:
                f.write('''import os

SKETCH_DIR = "sketches"

def list_sketches():
    return [f for f in os.listdir(SKETCH_DIR) if f.endswith(".py")]

if __name__ == "__main__":
    sketches = list_sketches()
    if not sketches:
        print("⚠️ No sketches found! Add some in the 'sketches/' folder.")
    else:
        print("Available Sketches:")
        for idx, sketch in enumerate(sketches, 1):
            print(f"{idx}. {sketch}")
        choice = input("Enter the sketch number to run: ")
        try:
            sketch_file = sketches[int(choice) - 1]
            sketch_path = os.path.join(SKETCH_DIR, sketch_file)
            exec(open(sketch_path).read())
        except (IndexError, ValueError):
            print("Invalid choice. Exiting.")
''')

            typer.echo("✅ Created template structure with directories, README, and main.py")
    
    except FileExistsError:
        typer.echo(f"❌ Error: Sketchbook '{name}' already exists at {path}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Error creating sketchbook: {str(e)}", err=True)
        raise typer.Exit(code=1)

# You can add more commands like this:
@app.command()
def list():
    """List all sketchbooks in the current directory."""
    typer.echo("Listing sketchbooks...")
    # Implementation here

if __name__ == "__main__":
    app()