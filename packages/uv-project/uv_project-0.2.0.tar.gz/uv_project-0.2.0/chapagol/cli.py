import os
import typer

app = typer.Typer()


@app.command()
def list_files_and_dirs():
    """List all directories and files in the current directory."""
    current_directory = os.getcwd()
    typer.echo(f"Current Directory: {current_directory}\n")

    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        if os.path.isdir(item_path):
            typer.echo(f"[DIR]  {item}")
        else:
            typer.echo(f"[FILE] {item}")


if __name__ == "__main__":
    app()