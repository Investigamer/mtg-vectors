# Magic the Gathering Vectors
A repository of Magic the Gathering SVG (vector) files for set, watermark, and miscellaneous symbols.

# Python Scripts
This repository includes configuration for a small Python project, the scope of which is mostly contained 
within the `src` directory and executed via the `scripts.py` file. These Python scripts provide utilities 
to check our existing symbol catalogue against a variety of Magic the Gathering data sources to detect when 
new symbols emerge that haven't been catalogued in this repository.

# Python Setup (Poetry)
1. Install poetry if you don't have it. The favorite method for installing poetry is using pipx to install poetry
to your main Python environment.
    ```shell
    # NOTE: If `py` doesn't work, replace `py` commands with `python` or `python3`.
    # 1: Install pipx and ensure path.
    py -m pip install --user pipx
    py -m pipx ensurepath
    
    # 2: Install poetry.
    pipx install poetry

    # 2.a: [Optional] Configure poetry to create virtual environments in-project (recommended).
    poetry config virtualenvs.in-project true
    
    # 3: Test that poetry works.
    poetry --version
    # Output: Poetry (version 1.7.0)
    ```
2. Clone the `mtg-vectors` repository somewhere on your system and install the project environment with Poetry.
    ```shell
    # 1: Clone and enter the project.
    git clone https://github.com/Investigamer/mtg-vectors.git
    cd mtg-vectors

    # 2: Install the poetry environment.
    poetry install
    ```
3. The project is now set up. You can launch our scripts one of two ways:
    ```shell
    # Option 1: Run `scripts.py` via poetry.
    poetry run scripts.py

    # Option 2: Enter the poetry environment shell, then run python files like normal.
    poetry shell
    python scripts.py
    ```
4. Have fun!

# Python Setup (Pip)
1. If you don't feel like using Poetry (you really should, it's great!) you can install the Python project using the 
good old fashion pip. First lets clone the `mtg-vectors` repository somewhere on your system:
    ```shell
    # Clone and enter the project.
    git clone https://github.com/Investigamer/mtg-vectors.git
    cd mtg-vectors
    ```
2. Next, create a Python virtual environment (highly recommended) and install our dependencies to it.
    ```shell
    # 1: Optional, but highly recommended: Create a virtual environment ...
    py -m venv .venv
    # Then enter the environment with one of these commands.
    .venv/scripts/activate # For Windows
    source .venv/bin/activate # MacOS or Linux
   
    # 2: Install our project dependencies.
    pip install -r requirements.txt
    ```
3. To launch our `scripts.py` file, just use `python scripts.py`, just remember you will need to be *inside the 
virtual environment*. That means anytime you open a new shell/terminal, you will need to first enter the environment 
with one of the two commands above before you can run `scripts.py`.