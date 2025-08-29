# Legends Launcher

A custom launcher for Project Legends, built with Python and [customtkinter](https://github.com/TomSchimansky/CustomTkinter).  
It manages your Brawl ISO, launches Dolphin, and provides update and settings management.

## Features

- First-time check for Brawl ISO (prompts user if not found)
- Custom logo and background
- Launch and update Dolphin
- **Automatic and manual update options**
- **Update channel selection: Main (GitHub Releases) or Alpha (GitHub Master branch)**
- **Update progress bar and restart after update**
- **Settings window with update preferences (auto/manual, channel)**
- **Modern UI using CustomTkinter (white background, black buttons)**

## Requirements

- Python 3.8+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Pillow](https://python-pillow.org/)
- `Dolphin.exe` in the project directory
- `background.png` and `legends_logo.png` in the project directory

## Setup

1. Clone this repository.
2. Install dependencies:
    ```
    pip install customtkinter pillow
    ```
3. Place your `Dolphin.exe`, `background.png`, and `legends_logo.png` in the project folder.
4. Run the launcher:
    ```
    python src/main.py
    ```

## Configuration

- On first launch, you will be prompted to select your Brawl ISO and choose update channel (Main/Alpha).
- The path and settings are saved in `config.ini` for future launches.
- Settings (including update mode and channel) can be changed via the Settings button in the launcher.

## Update System

- **Main build**: Uses GitHub Releases for updates.
- **Alpha build**: Uses the latest commit from the GitHub master branch.
- Checks for updates automatically (if enabled) or manually via the Update button.
- Shows a progress bar during download and restarts after update.

## License

MIT License
