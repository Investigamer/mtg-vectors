# Magic the Gathering Vectors
A repository of Magic the Gathering SVG (vector) files for set, watermark, and miscellaneous symbols. If you wish to 
contribute to this repository, please check our [missing vectors list](/docs/MISSING.md). This list is generated automatically every week 
to ensure the repository remains updated as new symbols are released.
<div align="center" markdown="1" style="font-size: large;">

   [![GitHub Release](https://img.shields.io/github/v/release/Investigamer/mtg-vectors?color=white)](https://github.com/Investigamer/mtg-vectors/releases/latest)
   ![GitHub last commit](https://img.shields.io/github/last-commit/Investigamer/mtg-vectors?label=last-updated&color=blue)
   [![GitHub License](https://img.shields.io/github/license/Investigamer/mtg-vectors?color=black)](https://www.tldrlegal.com/license/mozilla-public-license-2-0-mpl-2)
   ![Static Badge](https://img.shields.io/badge/python-3.10%E2%80%943.12-yellow?color=red)
   [![Discord](https://img.shields.io/discord/889831317066358815?label=discord&color=green)](https://discord.gg/magicproxies)

</div>

# 💌 How can I support the project?
Feel free to [join our community discord](http://discord.gg/magicproxies) where we test, improve, and release all kinds of awesome MTG related tools
and templates. Also, please consider supporting me on [Patreon](http://patreon.com/mpcfill) which pays for hosting costs, gives me time to expand
and maintain this repository and other API datasets, and helps me build a ton of cool stuff like 
[Proxyshop](https://github.com/Investigamer/Proxyshop), [MTG Art Downloader](https://github.com/Investigamer/mtg-art-downloader), 
the [Hexproof API](https://api.hexproof.io/docs) and more! If Patreon isn't your thing, you can also buy 
me a coffee [via PayPal](https://www.paypal.com/donate/?hosted_button_id=D96NBC6ZAJ8H6). Thanks so much to our awesome supporters!

# Python CLI
This repository includes a small Python project, the scope of which is contained 
within the `src` directory. This project provides a variety of CLI commands for gathering Scryfall data,
testing our existing SVG catalogue against existing sets, generating a `MISSING.md` file tracking symbols
currently missing from the repository, generating a symbol manifest file, and building a zip package that
can be distributed to outside apps when the repository is updated.

# Python Setup (Poetry)
We use `uv` for managing the project environment, dependencies, etc. If you plan to contribute to the project using `uv` is essential.
1. [Install](https://docs.astral.sh/uv/getting-started/installation/) `uv` if you don't have it (for Windows I recommend installing via `scoop`).
2. Clone the `mtg-vectors` repository somewhere on your system and sync with `uv`.
    ```shell
    git clone https://github.com/Investigamer/mtg-vectors.git
    cd mtg-vectors
    uv sync --extra dev
    ```
3. The project is now set up. You can now run our utility scripts via the CLI:
    ```shell
    # List the command groups available
    uv run vectors --help
   
    # List the test commands available
    uv run vectors test --help
    
    # List the build commands available
    uv run vectors build --help
    ```

# Symbol Optimization
This project supports an optimization workflow which is executed anytime a new package is built for
distribution. To use this optimization workflow locally, you'll need both Inkscape and SVGO. You can install
Inkscape on any operating system by visiting their website. You can install SVGO to this project locally using 
`npm install`, or you can install SVGO to your global node installation with `npm install --global svgo`. To run 
the optimization workflow, use `vectors build optimized` within the virtual environment.

# Design Standards
1. Try to create symbols from scratch in a software like Adobe Illustrator, using a WoTC official rasterized asset as a 
guide. SOMETIMES you can use the Scryfall SVG linked next to an item in the `MISSING.md` reference file as a starting 
place, but do keep in mind Scryfall-provided SVG icons can often be inaccurate or poorly created.
2. For rarity colors, you must either sample colors from a WoTC official raster asset, or use the commonly held rarity 
colors from previous symbols. Please note that the rotation and spectrum of the gradient changes from symbol to symbol, 
please try to replicate the look of the specific symbol you are re-creating.
3. For non-rarity colors present in the symbol, always sample from an official WoTC provided raster asset. Don't just wing it.
4. When creating a new symbol, we ask that you please generate at-minimum these rarities: `WM, C, U, R, M, T`
5. I know the "T" rarity is only used in a handful of sets, but we try to maintain this rarity across the board for the
benefit of custom card designers. WM represents the "watermark" version of a set symbol and should have no outline 
(one solid black layer).
6. When you are finished with an SVG file, we recommend you export it with **no transparent margin/space around
the symbol**. Do not save the file as a symbol inside a larger transparent bounding box, or an art board that is larger than the
symbol itself. If using Illustrator, join the symbol layers into **one group**, select that group, and Right Click -> Export 
Selection.

# Data Standards
1. All real card data is gathered from Scryfall, and with _very few_ exceptions we try to use Scryfall equivalent naming 
conventions when dealing with symbol mapping, naming, sorting, etc.
2. For data files (confined to the `/data/` directory), we prefer to use the human-readable YAML `.yml` format.
3. For the manifest file `manifest.json`, we prefer to use JSON `.json` for its unrivaled performance, since this file 
is application-focused.
4. All vector assets are located in the `/svg/` directory, currently separated into two categories:
   - 'Set' Symbols, those found on the right hand side of a card's typeline.
   - 'Watermark' Symbols, those found in the textbox of certain cards, behind the rules text.
5. All optimized vector assets are located in the `/svg/optimized/` directory. These are versions of the original SVG
assets which have been normalized for use across different applications, with the source markup text minified for 
reduced file size. We recommend you use the optimized version of the catalog in any real world applications.
6. For user reference or documentation files (currently just `MISSING.md`), we prefer the widely supported and formatting rich
Markdown `.md` format.
7. When interpreting inconsistencies or undesirable mappings in Scryfall data, we consider the following:
   - Did Scryfall map the incorrect symbol because the real cards use a mix of different symbols?
   - Did Scryfall map the incorrect symbol because the symbol changed after the set was printed?
   - Did Scryfall map the incorrect symbol because they don't have the asset and never bother to add it?
   - Did Scryfall map the incorrect symbol because of purely user error?
   - Is there a symbol we have that can act as a clean replacement for the incorrect Scryfall mapping?

# The Symbol Manifest File
The project manifest (`manifest.json`) is used to track changes to the repository and help other applications
accurately map SVG assets to Magic the Gathering data. The manifest contains the following data sections:
### Meta
- `date` Date when the current manifest was generated, in `YYYY-MM-DD` format.
- `version` The version of the current manifest. Combines the project version (semVer) and date this manifest was 
generated e.g. `0.1.0+20240101`.
- `uri` URL pointing to the live hosted ZIP package of all vectors catalogued in the repository at the time this manifest was generated.
### Set
- `aliases` A dictionary mapping icon codes to the properly recognized universal alias for that icon code. See [Data Files](#data-files).
- `routes` A dictionary mapping set codes to replacement symbol codes. Typically, a set is assigned a manual routing in this 
dictionary because in our view Scryfall's provided icon for this set is incorrect. See [Data Files](#data-files).
- `symbols` A dictionary of all symbol codes found in this repository mapped to a list of rarities currently supported by
that symbol.
### Watermark
- `routes` A dictionary reserved for mapping watermarks in the future, currently unused.
- `symbols` A list of currently recognized watermark symbol names.

# Data Files
This repository contains a few data files which track helpful information relating to Scryfall's data sets and how this 
project maps symbols to MTG data to better match real world cards.

### Set Symbols
1. **[alias.yml](data/set/alias.yml)**—Tracks Scryfall "icon" resources that have multiple codes or have codes which require an alias to 
maintain compatibility across operating systems.
2. **[empty.yml](data/set/empty.yml)**—Tracks a list of sets that have no defined icon on Scryfall.
3. **[ignored.yml](data/set/ignored.yml)**—Tracks a list of directory names in our symbol catalog that are not recognized icon codes on Scryfall.
4. **[mixed.yml](data/set/mixed.yml)**—Tracks a list of sets where cards have a variety of different symbols.
5. **[routes.yml](data/set/routes.yml)**—Tracks a dictionary of set codes manually routed to symbol codes that defer from Scryfall's mapping.

### Watermarks
1. **[ignored.yml](data/watermark/ignored.yml)**—Tracks a list of watermark names recognized by Scryfall that do exist in this catalog, but don't share the same filename.
2. **[mixed.yml](data/watermark/mixed.yml)**—Tracks a list of watermark names recognized by Scryfall that represent multiple different 
symbols. We plan to implement a strategy for mapping each watermark subset to the appropriate cards.