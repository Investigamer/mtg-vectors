# Magic the Gathering Vectors
A repository of Magic the Gathering SVG (vector) files for set, watermark, and miscellaneous symbols. If you wish to 
contribute to this repository, please check our [missing vectors list](/docs/MISSING.md). This list is generated automatically every week 
to ensure the repository remains updated as new symbols are released.
<div align="center" markdown="1" style="font-size: large;">

   [![GitHub file size in bytes](https://img.shields.io/github/size/Investigamer/mtg-vectors/package.zip?label=latest-package&color=white)](https://raw.githubusercontent.com/Investigamer/mtg-vectors/main/package.zip)
   ![GitHub last commit](https://img.shields.io/github/last-commit/Investigamer/mtg-vectors?label=last-updated&color=blue)
   [![GitHub License](https://img.shields.io/github/license/Investigamer/mtg-vectors?color=black)](https://www.tldrlegal.com/license/mozilla-public-license-2-0-mpl-2)
   ![Static Badge](https://img.shields.io/badge/python-3.10%E2%80%943.12-yellow?color=red)
   [![Discord](https://img.shields.io/discord/889831317066358815?label=discord&color=green)](https://discord.gg/magicproxies)

</div>

# Python CLI
This repository includes a small Python project, the scope of which is contained 
within the `src` directory. This project provides a variety of CLI commands for gathering Scryfall data,
testing our existing SVG catalogue against existing sets, generating a `MISSING.md` file tracking symbols
currently missing from the repository, generating a symbol manifest file, and building a zip package that
can be distributed to outside apps when the repository is updated.

# Python Setup (Poetry)
We like to use Poetry for managing the project environment, dependencies, etc. It is highly recommended to install 
setup this project using the Poetry method, ESPECIALLY if you plan to contribute to the project. If you wish to set up 
the project without using Poetry, skip to [this](#python-setup-without-poetry) section.
1. Install poetry if you don't have it.
    ```shell
    # 1: Install pipx and ensure path.
    py -m pip install --user pipx
    py -m pipx ensurepath
    
    # 2: Install poetry and check that it works
    pipx install poetry
    poetry --version

    # 3: [Recommended] Configure poetry to create virtual environments in-project.
    poetry config virtualenvs.in-project true
    ```
2. Clone the `mtg-vectors` repository somewhere on your system and install the project environment with Poetry.
    ```shell
    # 1: Clone and enter the project.
    git clone https://github.com/Investigamer/mtg-vectors.git
    cd mtg-vectors

    # 2: Install the poetry environment.
    poetry install
    ```
3. The project is now set up. You can now run our utility scripts via the CLI:
    ```shell
    # See the "test" scripts available
    vectors test --help

    # See the "build" scripts available
    vectors build --help
    ```

# Python Setup (Without Poetry)
1. If you don't feel like using Poetry (you really should, it's great!) you can install the Python project using the 
good old fashion pip. First lets clone the `mtg-vectors` repository somewhere on your system:
    ```shell
    # Clone and enter the project.
    git clone https://github.com/Investigamer/mtg-vectors.git
    cd mtg-vectors
    ```
2. Next, create a Python virtual environment (highly recommended) and install our dependencies to it.
    ```shell
    # 1: Create a virtual environment
    py -m venv .venv
   
    # #2: Enter the virtual environment
    .venv/scripts/activate # For Windows
    source .venv/bin/activate # MacOS or Linux
   
    # 2: Install our project dependencies.
    pip install -r requirements.txt
    ```
3. The project is now set up. You can now run our utility scripts via the CLI:
    ```shell
    # See the "test" scripts available
    py src/cli.py test --help

    # See the "build" scripts available
    py src/cli.py build --help
    ```

# Design Standards
1. Try to create symbols from scratch in a software like Adobe Illustrator, using a WoTC official rasterized asset as a 
guide. SOMETIMES you can use the Scryfall SVG linked next to an item in the `MISSING.md` reference file as a starting 
place, but do keep in mind Scryfall-provided SVG icons can often be inaccurate or poorly created.
2. For rarity colors, you must either sample colors from a WoTC official raster asset, or use the commonly held rarity 
colors from previous symbols. Please note that the rotation and spectrum of the gradient changes pretty frequently over 
different symbols, please try to replicate the look of the specific symbol you are re-creating.
3. For non-rarity colors present in the symbol, always sample from an official WoTC provided raster asset. Don't just wing it.
4. When creating a new symbol, we ask that you please generate at-minimum these rarities: `WM, C, U, R, M, T`
5. I know that the "T" rarity is only used in a handful of sets, but we try to maintain this rarity across the board for the
benefit of custom cards, designing custom cubes, and other creative activities. WM represents the "watermark" version of a set
symbol and should have no outline (one solid black layer).
5. **PLEASE**, when you are finished with an SVG file, make sure to save or export it with **no transparent margin/space around
the symbol**. Do not save the file as a symbol inside a larger transparent bounding box, or an art board that is larger than the
symbol itself. If using Illustrator, join the symbol layers into **one group**, select that group, and Right Click -> Export 
Selection. We are trying to enforce all symbols having no extra margin space.

# Data Standards
1. All real card data is gathered from Scryfall, and with _very few_ exceptions we try to use Scryfall equivalent naming 
conventions when dealing with symbol mapping, naming, sorting, etc.
2. For data files (confined to the `/data/` directory), we prefer to use the human-readable YAML `.yml` format.
3. For the manifest file `manifest.json`, we prefer to use JSON `.json` for its unrivaled performance, since this file is application-focused.
4. All vector assets are located in the `/svg/` directory, currently separated into two categories:
   - 'Set' Symbols, those found on the right hand side of a card's typeline.
   - 'Watermark' Symbols, those found in the textbox of certain cards, behind the rules text.
5. For user reference or documentation files (currently just `MISSING.md`), we prefer the widely supported and formatting rich
Markdown `.md` format.
6. When interpreting inconsistencies or undesirable mappings in Scryfall data, we consider the following:
   - Did Scryfall map the incorrect symbol because the real cards use a mix of different symbols?
   - Did Scryfall map the incorrect symbol because the symbol changed after the set was printed?
   - Did Scryfall map the incorrect symbol because they don't have the asset and never bother to add it?
   - Did Scryfall map the incorrect symbol because of purely user error?
   - Is there a symbol we have that can act as a clean replacement for the incorrect Scryfall mapping?

# The Symbol Manifest File
The manifest for this repository (`manifest.json`) contains the following information:
1. `meta` — This key tracks metadata about the current state of the repository.
   - `date` — The date when the current manifest was generated.
   - `version` — The version of the current manifest, combines the version of the repository and date this manifest was generated.
   - `uri` — URL pointing to the live hosted ZIP package of all vectors catalogued in the repository at the time this manifest was generated.
2. `set` — This key tracks all information pertaining to "set" symbol vectors.
   - `route` — A dictionary mapping some set codes to a specific symbol code. Typically, a set is assigned a manual routing in this 
dictionary because in our view Scryfall's provided icon for this set is incorrect. We also try to enforce one code for all symbols in 
the repository, and Scryfall has a few cases where the same icon is given multiple icon names. In these cases we try to choose the most
sensible of these names and re-route any duplicates to the preferred one. See the [Other Data Files](#other-data-files) section for more info.
   - `symbols` — A dictionary of all symbol codes found in this repository mapped to a list of rarities currently supported by
that symbol.
3. `watermark` — This key tracks all information pertaining to "watermark" symbol vectors.
   - `routes` — A dictionary which might map certain watermark names to other watermark names. Currently empty.
   - `symbols` — A list of currently recognized watermark symbol names.

# Other Data Files
1. `/set/alies.yml` — Tracks Scryfall "icon" resources that have multiple codes. The key represents the code we've chosen
as "canon" for that symbol. The value is a list of all codes Scryfall has associated with this symbol at varying times.
2. `/set/corrected.yml` — Tracks sets that Scryfall has assigned a seemingly incorrect icon code to. The key represents
the set's "code", the value represents the symbol code we have chosen to route this set to.
3. `/set/empty.yml` — Tracks a list of sets that have no defined icon on Scryfall.
4. `/set/ignored.yml` — Tracks s list of directory names in our symbol catalog that are not recognized icon names on Scryfall.
5. `/set/mixed.yml` — Tracks a list of sets that have a variety of different symbols, please note that generally Scryfall will 
assign the "DEFAULT" code to these, but not always. In the future we plan to create additional mappings that allow users to 
route individual cards in a given set to specific symbols to help deal with this scenario.
6. `/set/rarities.yml` — Tracks all the rarities recognized by this repository.
7. `/set/routes.yml` — Tracks a dictionary of set codes manually routed to symbol codes. Keys are valid Scryfall set codes, 
values are symbol codes from our catalog. This dictionary is the culmination of many hours of analyzing Scryfall set data, 
it was migrated to this project from my app [Proxyshop](https://github.com/Investigamer/Proxyshop) and heavily modified 
thereafter to meet the requirements of the project. It is compiled by synthesizing, combining, and interpolating the other
data files into a unified mapping, only re-routing sets which have a different icon code on Scryfall (for any reason). The 
`routes` dictionary in our generated `manifest.json` is sourced from this dictionary at the time the manifest is generated.
8. `/watermark/ignored.yml` — Tracks a list of watermark names recognized by Scryfall that do exist in this catalog, but don't
share the same filename.
9. `/watermark/mixed.yml` — Tracks a list of watermark names recognized by Scryfall that represent multiple different 
symbols. We need to formalize a methodology for mapping each specific occurrence of this watermark name to the appropriate 
vector asset.
