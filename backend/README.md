# Backend

## Installation

### Setup

1.  Have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed (package manager). `pip install uv` on windows

    -   [uv guide](https://docs.astral.sh/uv/guides/projects/)

2.  Have python installed. You can use uv for this: `uv python install 3.12`
3.  Navigate to the `backend` directory in your terminal.
4.  Run `uv venv` to create a virtual environment.

### Running

1.  Activate the virtual environment

    -   `source .venv/bin/activate` (Linux/macOS)
    -   `.venv\Scripts\activate` (Windows)

2.  Run the application: `uv run app.py`
3.  Frontend should be run in another terminal
