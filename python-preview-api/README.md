## What is this folder?
Rosetic Studio's app preview is powered by a real, running backend, not a mockup. This Python API is the backend that runs behind the preview inside Studio, and it is included in every generated project regardless of the API you selected during onboarding.

- **If you selected Python during onboarding**, this is your production backend and where your real development should happen.
- **If you selected a different API (for example C# or Java)**, this folder is a copy of the preview backend only. Nothing in your generated code uses it, and your selected API lives in its own folder next to this one. It is safe to delete this folder, but note that it will be regenerated on subsequent code generations.

Running the preview directly on the C# and Java APIs is on the roadmap. Once that is in place, newly generated projects will contain a single backend folder for your chosen API.

## Requirements
- Python 3.11 or higher

## Setup
Inside the project folder:

1. Create a .env file or rename .env.example to .env and add your database connection string:
    ```
    DATABASE_URI={Database Connection String}
    ```

2. Create a virtual environment:

        python -m venv .venv
    or
    
        uv venv

3. Activate it
    - Linux, macOS: 

    ```sh
    source .venv/bin/activate
    ```

    - Windows Powershell:

    ```powershell
    .venv\Scripts\Activate.ps1
    ```

    - Windows/Git Bash:

    ```sh
    source .venv/Scripts/activate
    ```

4. Install packages

        Dependencies and tool configuration live in `pyproject.toml`. Pick one of:

    - pip (runtime + dev tools, editable):

            pip install -e . --group dev

        For runtime only, `pip install -e .`

    - uv (auto-creates `.venv`, faster, produces a lockfile):

            uv sync

        For runtime only, `uv sync --no-dev`


 * On macOS you might need to reactivate the venv before running the API
 
        source .venv/bin/activate

5. Run API

        fastapi dev main.py

6. When done deactivate virtual environment:

        deactivate



For more info: https://fastapi.tiangolo.com/virtual-environments/


## Additional Requirements for macOS and Linux

Install `unixodbc` (required for `pyodbc` for macOS & Linux):

- (Linux) `apt-get install unixodbc`
- If you have Homebrew/Linuxbrew: `brew install unixodbc`
- If you don't have Homebrew: Download the `unixODBC` source code from the official website: [http://www.unixodbc.org/](http://www.unixodbc.org/)

## API Documentation
The API documentation is available at `/docs`

## API Testing
There are extensive unit tests for the API, located in the `/tests` folder. You can run them with the following command:

        pytest
or run a specific test:

        pytest path/to/test_file.py

run with a coverage report:
        
        pytest --cov-report term --cov=.