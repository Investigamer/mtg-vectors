## v0.7.1 (2024-08-12)

### Fix

- **build**: Ensure proper URI is entered into the manifest

## v0.7.0 (2024-08-11)

### Feat

- **symbols**: New sets: DSC, DSK, FDN, J25, MB2

### Refactor

- **workflows**: Remove push activation

## v0.6.11 (2024-07-27)

### Refactor

- **svg**: Add repaired symbols
- **svg**: Temporarily remove anomalous symbols

## v0.6.10 (2024-07-27)

### Refactor

- **workflows**: Update formatting of release body
- **git**: Ensure manifest isn't committed to repo
- **naming**: Re-add properly named symbols which encountered filename issue
- **naming**: Remove optimized symbols to fix naming issue with git

## v0.6.9 (2024-07-25)

### Refactor

- **svg**: Remove eroneous files
- **workflows**: Minor tweaks
- **commands**: Update commands and command utilities using new schema system, data files, and build system
- **symbols,schema**: Rework set symbol utilities using new schema structures, remove deprecated files
- **watermarks**: Rework watermark utilities
- **github**: Deprecate unneeeded workflow, update build workflow
- **data**: Major rework of data files, deprecate files no longer needed
- **cleanup**: Remove unnecessary files and generate new docs
- **svg**: Relocate unused symbols, add new optimized symbols path
- **utils**: Minor refactoring
- **routes**: Commit final update before planning deprecation of manual routes

## v0.6.8 (2024-07-09)

### Fix

- **workflow**: Minor typo in github action

### Refactor

- **workflows**: Improve optimization workflow
- **optimize-svgs.yml**: Make sure to pull changes

## v0.6.7 (2024-06-26)

### Fix

- **workflows**: Make sure to fetch tags
- **workflows**: Ensure cz command run from poetry
- **cli**: Fix incorrect CLI entrypoint
- **build-all**: Try to correct issue with poetry/pipx
- **workflows**: Correct typo, rework flow
- **typo**: Fix workflow typo

### Refactor

- **workflows**: Remove commands.txt from final commit, make a few small changes
- **workflows**: Rename file
- **poetry**: Update poetry deps, build new manifest, package, and docs
- **svg/set**: Add lots of new symbols!

## v0.6.6 (2024-06-01)

### Refactor

- **cli,poetry**: Minor cli refactoring, update poetry.lock deps

## v0.6.5 (2024-04-02)

### Fix

- **symbols/set**: PR #1 from jordi735/main, crop and clean set symbol SVG's

### Refactor

- **symbols/set**: Add new symbols: BLB, MC3, OTJ. Update symbols: ACR, MH3

## v0.6.4 (2024-02-26)

### Refactor

- **symbols/set**: Added new symbols: MH3

## v0.6.3 (2024-02-26)

### Refactor

- **symbols/set**: New symbol: ACR
- **svg/symbols,README**: Add new rarities for MED, update README

## v0.6.2 (2024-02-23)

### Refactor

- **symbols/set**: Add missing symbols: PLANESWALKER, PAPAC, PEURO

## v0.6.1 (2024-02-23)

### Refactor

- **symbols/set**: Add new symbols: CLU, RIN, REN

## v0.6.0 (2024-02-22)

### Feat

- **CLI**: Implement new CLI to replace basic "scripts" file. Commands include building manifest and docs, as well as basic tests

### Refactor

- **README,constants,utils**: General refactoring after implementing CLI and use of the "omnitils" package
- **requirements.txt**: Update project files, poetry lock, and add "requirements.txt"
- **symbols/set**: Add missing rarities for various symbols, correct margin spacing on various symbols

## v0.5.2 (2024-01-24)

### Refactor

- **symbols/set**: Add MKC symbols, remove old missing.yml file
- **manifest**: Update collection manifest

## v0.5.1 (2024-01-18)

### Refactor

- **set**: New symbol "MKM", updated symbol "RVR"

## v0.5.0 (2024-01-09)

### Feat

- **watermark**: Add many new watermarks, most modified from https://github.com/andrewgioia/mana

### Fix

- **generate_markdown_missing**: Fix issue where special characters in scryfall link would mutate the query
- **MISSING.md**: Update MISSING.md with fixed methodology
- **get_missing_symbols_set_rarities**: Prevent false positive on WM entries

### Refactor

- **get_missing_symbols_watermark**: Ensure ignored watermarks are not included in the "MISSING.md" generator
- **WMPath,WMData**: Add watermark constant objects
- **data**: Start tracking "mixed" and "ignored" watermark data
- **manifest**: Update manifest version

## v0.4.0 (2023-12-10)

### Feat

- **scripts**: Add a symbols rarity check to the MISSING.md generator
- **scripts**: Add function for auto-generating a "MISSING.md" record that tracks missing vector symbols
- **python**: Rewrote the python subproject and implemented a better mechanism for discovering uncaptured symbols

### Refactor

- **package**: Remove unneeeded package subdir

## v0.3.0 (2023-12-04)

### Feat

- **manifest**: Implement manifest generation script

### Refactor

- **data**: Rework symbol map naming to match Scryfall, move alternates to .alt directory
- **pyproject.toml**: Updated changelog settings and removed broken commitizen templating

## v0.2.0 (2023-11-30)
### Feat
    
- **Watermarks**: Added initial watermark SVG repository.

## v0.1.0 (2023-11-30)
### Initial Release