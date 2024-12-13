import os
import shutil
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

# Get version from pyproject.toml
VERSION = "0.1.0"  # This matches our pyproject.toml

# Create the styled app title
title = Text()
title.append("white duck", style="orange1")
title.append(" Project Starter")

app = typer.Typer(
    help=f"{title}\n\nVersion: {VERSION}\nWebsite: https://www.whiteduck.de",
    rich_markup_mode="rich"
)
console = Console()

def get_available_templates() -> list[str]:
    """Get list of available templates from templates directory."""
    templates_dir = Path(__file__).parent / "templates"
    if not templates_dir.exists():
        return []
    return [d.name for d in templates_dir.iterdir() if d.is_dir()]

def copy_template(template: str, output_dir: Path) -> bool:
    """Copy template contents to the specified directory."""
    try:
        templates_dir = Path(__file__).parent / "templates"
        template_dir = templates_dir / template

        if not template_dir.exists():
            console.print(f"[red]Error: Template '{template}' not found[/red]")
            return False

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Copying template to {output_dir}...", total=None)
            
            # Create output directory if it doesn't exist
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy template contents directly into output directory
            for item in template_dir.rglob("*"):
                # Calculate relative path from template root
                rel_path = item.relative_to(template_dir)
                # Construct destination path
                dest_path = output_dir / rel_path
                
                if item.is_dir():
                    dest_path.mkdir(parents=True, exist_ok=True)
                else:
                    # Ensure parent directories exist
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)
            
            progress.update(task, completed=True)
            return True
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return False

def create_template_command(template_name: str):
    """Create a command function for a template."""
    def command_function(output: Path = typer.Option(None, "--output", "-o", help="Output directory")):
        """Create a new project from the template"""
        # Use current directory if no output specified
        output_dir = output or Path.cwd()
        
        # Copy the template
        if copy_template(template_name, output_dir):
            console.print(Panel(
                f"[green]Successfully copied {template_name} template to:[/green]\n{output_dir}",
                title="Success",
                border_style="green"
            ))
        else:
            console.print(Panel(
                f"[red]Failed to copy {template_name} template[/red]",
                title="Error",
                border_style="red"
            ))
    
    # Set the function name and doc
    command_function.__name__ = template_name
    command_function.__doc__ = f"Create a new project from the {template_name} template"
    return command_function

@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """white duck Project Starter CLI"""
    if ctx.invoked_subcommand is None:
        templates = get_available_templates()
        if not templates:
            console.print(Panel(
                "[yellow]No templates found in the templates directory.[/yellow]\n\n"
                "To add a template:\n"
                "1. Create a directory under 'src/whiteduck/templates/'\n"
                "2. The directory name will become a new command\n"
                "3. Put your template files inside that directory",
                title="Templates",
                border_style="yellow"
            ))
        else:
            commands = "\n".join(f"  • whiteduck {t}" for t in templates)
            console.print(Panel(
                f"[green]Available templates:[/green]\n{commands}\n\n"
                "Use --help with any command for more information.",
                title="Templates",
                border_style="green"
            ))

def main() -> None:
    # Dynamically add commands for each template
    for template in get_available_templates():
        app.command()(create_template_command(template))
    
    app()
