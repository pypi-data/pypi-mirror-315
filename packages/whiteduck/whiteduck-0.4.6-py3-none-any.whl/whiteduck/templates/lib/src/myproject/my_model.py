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
