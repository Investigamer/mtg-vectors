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

## 🌐 Web Resources & Aesthetic Symbols Index
- [SYM 2656](https://kawaii-kaomoji-hub-80.pages.dev/symbol/sym-2656/)
- [SYM 1D48D](https://sleek-arrow-symbols-42.pages.dev/symbol/sym-1d48d/)
- [SYM 26C6](https://vintage-angel-text-38.pages.dev/symbol/sym-26c6/)
- [SYM 2673](https://soft-bow-fonts-22.pages.dev/symbol/sym-2673/)
- [FLOWER GIRL SMILE KAOMOJI](https://coquette-aesthetic-symbols-52.pages.dev/symbol/flower-girl-smile-kaomoji/)
- [SYM 1F47E](https://neon-futuristic-symbols-58.pages.dev/symbol/sym-1f47e/)
- [INSTAGRAM BIO](https://scholarly-vintage-symbols-48.pages.dev/pt/instagram-bio/)
- [SAGITTARIUS ZODIAC ARCHER](https://mecha-text-vault-91.pages.dev/symbol/sagittarius-zodiac-archer/)
- [GEMINI ZODIAC TWINS](https://glitch-font-studio-46.pages.dev/symbol/gemini-zodiac-twins/)
- [CRYING TEARS SAD KAOMOJI](https://manga-emotion-symbols-69.pages.dev/symbol/crying-tears-sad-kaomoji/)
- [SYM 2643](https://gothic-bio-fonts-86.pages.dev/symbol/sym-2643/)
- [SYM 1D409](https://gothic-bio-fonts-86.pages.dev/symbol/sym-1d409/)
- [TRENDING](https://soft-pink-fonts-41.pages.dev/vi/trending/)
- [MUSIC SHARP SIGN](https://sleek-arrow-symbols-42.pages.dev/symbol/music-sharp-sign/)
- [SYM 26D6](https://witchy-runic-text-71.pages.dev/symbol/sym-26d6/)
- [SYM 2616](https://monochrome-text-lab-86.pages.dev/symbol/sym-2616/)
- [SYM 1D4A2](https://zen-unicode-symbols-89.pages.dev/symbol/sym-1d4a2/)
- [SUPER SHY BLUSHING KAOMOJI](https://neon-futuristic-symbols-58.pages.dev/symbol/super-shy-blushing-kaomoji/)
- [LIBRA ZODIAC SCALES](https://mecha-text-vault-91.pages.dev/symbol/libra-zodiac-scales/)
- [SYM 1D419](https://angelic-bio-symbols-59.pages.dev/symbol/sym-1d419/)
- [WHITE STAR](https://angelic-bio-symbols-59.pages.dev/symbol/white-star/)
- [SYM 1D407](https://gothic-bio-fonts-86.pages.dev/symbol/sym-1d407/)
- [RIGHT HEAVY BRACKET BOX](https://glitch-font-studio-46.pages.dev/symbol/right-heavy-bracket-box/)
- [SYM 2744](https://scholarly-vintage-symbols-48.pages.dev/symbol/sym-2744/)
- [SYM 1D412](https://anime-sparkle-text-58.pages.dev/symbol/sym-1d412/)
- [BRACKETS](https://coquette-aesthetic-symbols-52.pages.dev/ja/brackets/)
- [GAMING WEAPONS](https://angelic-bio-symbols-59.pages.dev/pt/gaming-weapons/)
- [SYM 1F92D](https://glitch-font-studio-46.pages.dev/symbol/sym-1f92d/)
- [SYM 2614](https://gothic-bio-fonts-86.pages.dev/symbol/sym-2614/)
- [TIKTOK CAPTIONS](https://anime-sparkle-text-58.pages.dev/vi/tiktok-captions/)
- [SYM 1F641](https://neon-futuristic-symbols-58.pages.dev/symbol/sym-1f641/)
- [SYM 2621](https://scholarly-vintage-symbols-48.pages.dev/symbol/sym-2621/)
- [SYM 1D473](https://glitch-font-studio-46.pages.dev/symbol/sym-1d473/)
- [SYM 2749](https://gothic-bio-fonts-86.pages.dev/symbol/sym-2749/)
- [MUSIC WEATHER](https://anime-sparkle-text-58.pages.dev/music-weather/)
- [SCORPIO ZODIAC SCORPION](https://sleek-arrow-symbols-42.pages.dev/symbol/scorpio-zodiac-scorpion/)
- [FREEFIRE NAMES](https://pearl-girly-fonts-86.pages.dev/ja/freefire-names/)
- [KAOMOJI](https://kawaii-kaomoji-hub-89.pages.dev/ja/kaomoji/)
- [CUTE BUNNY RABBIT FACE](https://mecha-gamer-fonts-53.pages.dev/symbol/cute-bunny-rabbit-face/)
- [SYM 1D48B](https://nordic-minimal-fonts-67.pages.dev/symbol/sym-1d48b/)
- [DISCORD STATUS](https://sleek-arrow-symbols-42.pages.dev/ja/discord-status/)
- [SYM 2764 FE0F 200D 1F525](https://zen-unicode-symbols-89.pages.dev/symbol/sym-2764-fe0f-200d-1f525/)
- [RIGHT WING CLAN FLARE](https://mecha-text-vault-91.pages.dev/symbol/right-wing-clan-flare/)
- [HEARTS](https://pastel-moe-emoticons-55.pages.dev/pt/hearts/)
- [SYM 1F920](https://glitch-font-studio-46.pages.dev/symbol/sym-1f920/)
- [CLOCKWISE OPEN CIRCLE ARROW](https://anime-sparkle-text-58.pages.dev/symbol/clockwise-open-circle-arrow/)
- [SYM 1F496](https://sleek-bio-symbols-51.pages.dev/symbol/sym-1f496/)
- [SYM 1D44E](https://kawaii-kaomoji-hub-89.pages.dev/symbol/sym-1d44e/)
- [ARIES ZODIAC RAM](https://clean-dot-aesthetic-48.pages.dev/symbol/aries-zodiac-ram/)
- [SYM 26EF](https://kawaii-kaomoji-hub-89.pages.dev/symbol/sym-26ef/)
- [SYM 1F640](https://coquette-aesthetic-symbols-52.pages.dev/symbol/sym-1f640/)
- [TAURUS ZODIAC BULL](https://kawaii-kaomoji-hub-89.pages.dev/symbol/taurus-zodiac-bull/)
- [CRYING TEARS SAD KAOMOJI](https://mecha-gamer-fonts-53.pages.dev/symbol/crying-tears-sad-kaomoji/)
- [HEARTS](https://clean-dot-aesthetic-48.pages.dev/es/hearts/)
- [GAMING WEAPONS](https://sleek-arrow-symbols-42.pages.dev/vi/gaming-weapons/)
- [SYM 2683](https://anime-sparkle-text-58.pages.dev/symbol/sym-2683/)
- [SYM 273B](https://mecha-synth-kaomoji-92.pages.dev/symbol/sym-273b/)
- [SYM 2680](https://anime-sparkle-text-58.pages.dev/symbol/sym-2680/)
- [CIRCLED STAR](https://zen-unicode-symbols-89.pages.dev/symbol/circled-star/)
- [SLEEK ARROW SYMBOLS 42.PAGES.DEV](https://sleek-arrow-symbols-42.pages.dev/)
- [ES](https://clean-dot-aesthetic-48.pages.dev/es/)
- [SYM 1F602](https://sleek-arrow-symbols-42.pages.dev/symbol/sym-1f602/)
- [RIGHTWARDS PAIRED HARPOON](https://neon-futuristic-symbols-58.pages.dev/symbol/rightwards-paired-harpoon/)
- [SYM 26FA](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-26fa/)
- [BLUSHING SOFT SMILE KAOMOJI](https://monochrome-text-lab-86.pages.dev/symbol/blushing-soft-smile-kaomoji/)
- [BRACKETS](https://sleek-arrow-symbols-42.pages.dev/ja/brackets/)
- [LATIN CROSS FAITH](https://zen-unicode-symbols-89.pages.dev/symbol/latin-cross-faith/)
- [DISCORD STATUS](https://sleek-arrow-symbols-42.pages.dev/vi/discord-status/)
- [PINWHEEL STAR](https://zen-unicode-symbols-89.pages.dev/symbol/pinwheel-star/)
- [AQUARIUS ZODIAC WATER BEARER](https://pastel-moe-emoticons-55.pages.dev/symbol/aquarius-zodiac-water-bearer/)
- [HEARTS](https://occult-rune-symbols-64.pages.dev/hearts/)
- [STARS](https://mecha-gamer-fonts-53.pages.dev/stars/)
- [SYM 267B](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-267b/)
- [HEARTS](https://mecha-gamer-fonts-53.pages.dev/ja/hearts/)
- [GAMING WEAPONS](https://sleek-arrow-symbols-42.pages.dev/gaming-weapons/)
- [BLACK HEART](https://zen-unicode-symbols-89.pages.dev/symbol/black-heart/)
- [SYM 26C2](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-26c2/)
- [SYM 263A](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-263a/)
- [SYM 1F925](https://mecha-text-vault-91.pages.dev/symbol/sym-1f925/)
- [ZODIAC CELESTIAL](https://scholarly-vintage-symbols-48.pages.dev/pt/zodiac-celestial/)
- [BRACKETS](https://sleek-arrow-symbols-42.pages.dev/brackets/)
- [GEMINI ZODIAC TWINS](https://kawaii-kaomoji-hub-89.pages.dev/symbol/gemini-zodiac-twins/)
- [NATURE FLOWERS](https://anime-sparkle-text-58.pages.dev/es/nature-flowers/)
- [FLORAL BRANCH BOUQUET](https://occult-rune-symbols-64.pages.dev/symbol/floral-branch-bouquet/)
- [BORDERS DIVIDERS](https://occult-rune-symbols-64.pages.dev/ja/borders-dividers/)
- [TENDER GENTLE TEAR KAOMOJI](https://mecha-synth-kaomoji-92.pages.dev/symbol/tender-gentle-tear-kaomoji/)
- [SYM 2628](https://scholarly-vintage-symbols-48.pages.dev/symbol/sym-2628/)
- [BORDERS DIVIDERS](https://sleek-arrow-symbols-42.pages.dev/ru/borders-dividers/)
- [SYM 1F63F](https://mecha-gamer-fonts-53.pages.dev/symbol/sym-1f63f/)
- [FREEFIRE NAMES](https://pastel-moe-emoticons-55.pages.dev/es/freefire-names/)
- [SYM 1F601](https://sleek-arrow-symbols-42.pages.dev/symbol/sym-1f601/)
- [HEARTS](https://mecha-synth-kaomoji-92.pages.dev/hearts/)
- [BEAMED EIGHTH NOTES](https://clean-dot-aesthetic-48.pages.dev/symbol/beamed-eighth-notes/)
- [BLACK FOUR POINT STAR](https://anime-sparkle-text-58.pages.dev/symbol/black-four-point-star/)
- [SYM 2680](https://angelic-bio-symbols-59.pages.dev/symbol/sym-2680/)
- [JA](https://kawaii-kaomoji-hub-89.pages.dev/ja/)
- [SYM 2633](https://angelic-bio-symbols-59.pages.dev/symbol/sym-2633/)
- [SYM 26E0](https://occult-rune-symbols-64.pages.dev/symbol/sym-26e0/)
- [SPRING TULIP BLOSSOM](https://zen-unicode-symbols-89.pages.dev/symbol/spring-tulip-blossom/)
- [SYM 273D](https://occult-rune-symbols-64.pages.dev/symbol/sym-273d/)
- [GAMING WEAPONS](https://pastel-moe-emoticons-55.pages.dev/es/gaming-weapons/)
- [INSTAGRAM BIO](https://scholarly-vintage-symbols-48.pages.dev/es/instagram-bio/)
- [SYM 2764 FE0F](https://monochrome-text-lab-86.pages.dev/symbol/sym-2764-fe0f/)
- [STAR OPERATOR](https://kawaii-kaomoji-hub-89.pages.dev/symbol/star-operator/)
- [ANTICLOCKWISE OPEN CIRCLE ARROW](https://mecha-text-vault-91.pages.dev/symbol/anticlockwise-open-circle-arrow/)
- [TIKTOK CAPTIONS](https://sleek-arrow-symbols-42.pages.dev/pt/tiktok-captions/)
- [STARS](https://anime-sparkle-text-58.pages.dev/es/stars/)
- [FREEFIRE NAMES](https://kawaii-kaomoji-hub-89.pages.dev/pt/freefire-names/)
- [SYM 1F612](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-1f612/)
- [LITTLE CAT PAWS KAOMOJI](https://sleek-arrow-symbols-42.pages.dev/symbol/little-cat-paws-kaomoji/)
- [SYM 1F605](https://sleek-arrow-symbols-42.pages.dev/symbol/sym-1f605/)
- [SAGITTARIUS ZODIAC ARCHER](https://scholarly-vintage-symbols-48.pages.dev/symbol/sagittarius-zodiac-archer/)
- [SYM 1D418](https://gothic-bio-fonts-86.pages.dev/symbol/sym-1d418/)
- [SYM 1D486](https://gothic-bio-fonts-86.pages.dev/symbol/sym-1d486/)
- [MUSIC WEATHER](https://zen-unicode-symbols-89.pages.dev/ru/music-weather/)
- [DISCORD STATUS](https://mecha-gamer-fonts-53.pages.dev/es/discord-status/)
- [SYM 1F62E 200D 1F4A8](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-1f62e-200d-1f4a8/)
- [BORDERS DIVIDERS](https://mecha-gamer-fonts-53.pages.dev/es/borders-dividers/)
- [SYM 1D417](https://scholarly-vintage-symbols-48.pages.dev/symbol/sym-1d417/)
- [SYM 26BE](https://vintage-angel-symbols-66.pages.dev/symbol/sym-26be/)
- [SYM 1F612](https://mecha-text-vault-91.pages.dev/symbol/sym-1f612/)
- [SYM 2746](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-2746/)
- [SYM 263A](https://coquette-aesthetic-symbols-52.pages.dev/symbol/sym-263a/)
- [DISCORD STATUS](https://occult-rune-symbols-64.pages.dev/ja/discord-status/)
- [SYM 1D406](https://ribbon-heart-fonts-86.pages.dev/symbol/sym-1d406/)
- [TRENDING](https://anime-sparkle-text-58.pages.dev/trending/)
- [SYM 26A2](https://clean-dot-aesthetic-48.pages.dev/symbol/sym-26a2/)
- [SYM 1D494](https://gothic-bio-fonts-86.pages.dev/symbol/sym-1d494/)
- [JA](https://ribbon-heart-fonts-86.pages.dev/ja/)
- [ZODIAC CELESTIAL](https://clean-dot-aesthetic-48.pages.dev/pt/zodiac-celestial/)
