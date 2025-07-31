# Build configuration for main and alpha builds

BUILD_TYPE = "main"  # Change to "alpha" for alpha build

SETTINGS = {
    "main": {
        "API_URL": "https://api.legends.com/",
        "DEBUG": False,
        "VERSION": "1.0.0",
        "DOLPHIN_RELEASE_API": "https://api.github.com/repos/project-slippi/dolphin/releases/latest",
        # Add more main build settings here
    },
    "alpha": {
        "API_URL": "https://alpha-api.legends.com/",
        "DEBUG": True,
        "VERSION": "1.0.0-alpha",
        "DOLPHIN_RELEASE_API": "https://api.github.com/repos/project-slippi/dolphin/releases/latest",
        # Add more alpha build settings here
    }
}

def get_setting(key):
    return SETTINGS[BUILD_TYPE][key]
