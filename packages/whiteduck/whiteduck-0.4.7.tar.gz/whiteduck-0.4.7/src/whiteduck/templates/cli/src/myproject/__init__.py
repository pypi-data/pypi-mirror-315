from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pydantic import BaseModel, Field, field_validator
from loguru import logger
import sys

# Configure loguru
logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

# Pydantic model for duck data
class Duck(BaseModel):
    name: str = Field(..., description="Name of the duck")
    color: str = Field(default="white", description="Color of the duck")
    age: Optional[int] = Field(None, description="Age of the duck in years")

    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('name cannot be empty')
        return v

def create_duck_table(ducks: list[Duck]) -> Table:
    """Create a rich table to display duck information."""
    table = Table(title="Duck Collection")
    table.add_column("Name", style="cyan")
    table.add_column("Color", style="magenta")
    table.add_column("Age", justify="right", style="green")
    
    for duck in ducks:
        table.add_row(
            duck.name,
            duck.color,
            str(duck.age) if duck.age else "Unknown"
        )
    return table

def main() -> None:
    """Main entry point for the White Duck CLI Starter demo."""
    console = Console()
    
    # Log some information
    logger.info("Starting White Duck CLI Starter demo")
    
    # Create some sample ducks
    ducks = [
        Duck(name="Donald", color="white", age=5),
        Duck(name="Daisy", color="white", age=4),
        Duck(name="Scrooge", color="white"),
    ]
    
    # Display welcome message in a panel
    console.print(Panel.fit(
        "[yellow]Welcome to White Duck CLI Starter![/yellow]\n"
        "A demo showcasing Rich, Pydantic, and Loguru",
        border_style="blue"
    ))
    
    # Log that we're about to display the ducks
    logger.debug("Preparing to display duck information")
    
    # Display duck information in a table
    console.print("\n[bold]Here are our ducks:[/bold]")
    console.print(create_duck_table(ducks))
    
    # Demonstrate error handling with loguru
    try:
        # Intentionally cause an error by creating an invalid duck
        invalid_duck = Duck(name="", color="invisible")
    except ValueError as e:
        logger.error(f"Failed to create invalid duck: {e}")
    
    logger.success("Demo completed successfully!")

if __name__ == "__main__":
    main()
