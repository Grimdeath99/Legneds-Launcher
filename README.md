# Legends Launcher

A custom launcher for Project Legends, built with Python and [customtkinter](https://github.com/TomSchimansky/CustomTkinter).  
It manages your Brawl ISO, launches Dolphin, and provides update and settings management.

## Features

- First-time check for Brawl ISO (prompts user if not found)
- Custom logo and background
- Launch and update Dolphin
- Settings window for build type and API configuration

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

- On first launch, you will be prompted to select your Brawl ISO.
- The path is saved in `config.ini` for future launches.
- Settings can be changed via the Settings button in the launcher.

## License

MIT License
