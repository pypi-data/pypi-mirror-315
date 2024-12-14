# White Duck CLI Starter

A demonstration project showcasing modern Python CLI development using Rich, Pydantic, and Loguru.

## Features

This starter project demonstrates:

- 🎨 **Rich** for beautiful terminal output
  - Styled panels and borders
  - Colored text and formatting
  - Structured tables for data display

- 🔒 **Pydantic** for data validation
  - Type-safe models
  - Field validation
  - Default values
  - Custom validators

- 📝 **Loguru** for sophisticated logging
  - Colored and formatted log output
  - Multiple log levels
  - Error handling
  - Timestamp integration

## Installation

The project uses modern Python packaging with `pyproject.toml` and requires Python 3.12 or higher.

Dependencies:
- rich>=13.9.4
- pydantic>=2.10.3
- loguru>=0.7.3

## Usage

Run the demo application:

```bash
uv run myproject
```

This will display:
1. A welcome message in a styled panel
2. Sample duck data in a formatted table
3. Various log messages demonstrating different log levels
4. Error handling demonstration

## Development

### Running Tests

The project includes a comprehensive test suite using pytest:

```bash
uv run pytest tests/test_myproject.py -v
```

Tests cover:
- Model validation
- Default value handling
- Error cases
- Table creation

### Project Structure

```
.
├── src/
│   └── myproject/
│       └── __init__.py      # Main application code
├── tests/
│   └── test_myproject.py    # Test suite
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

## Example Output

When you run the application, you'll see:
- A colorful welcome panel
- A table displaying duck information
- Formatted log messages
- Error handling demonstration

The application showcases a simple duck management system with:
- Duck creation with name, color, and age
- Data validation (e.g., non-empty names)
- Formatted table display
- Comprehensive logging
