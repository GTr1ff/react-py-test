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

            pip install -e ".[dev]"

    - uv (auto-creates `.venv`, faster, produces a lockfile):

            uv sync --extra dev

    For runtime only, drop `[dev]` / `--extra dev`.


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