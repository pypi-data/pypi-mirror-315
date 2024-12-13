"""Main module of the project."""

import uvicorn


def main() -> None:
    """Entrypoint for the project."""
    print("Hello from with-react-frontend!")
    uvicorn.run("myproject.api.routes:app", host="127.0.0.1", port=8000, reload=True)
