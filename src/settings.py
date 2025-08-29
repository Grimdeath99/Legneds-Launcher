# Build configuration for main and alpha builds

BUILD_TYPE = "main"  # Change to "alpha" for alpha build

SETTINGS = {
    "main": {
        "API_URL": "https://api.github.com/",
        "DEBUG": False,
        "DOLPHIN_RELEASE_API": "https://api.github.com/repos/Smash-Bros-Legends/releases/latest",
        "UPDATE_SOURCE": "github_releases",  # Use GitHub Releases for main
        "UPDATE_MODE": "auto",  # 'auto' or 'manual'
        # Add more main build settings here
    },
    "alpha": {
        "API_URL": "https://api.github.com.com/",
        "DEBUG": True,
        "DOLPHIN_RELEASE_API": "https://api.github.com/repos/Smash-Bros-Legends/commits/master",
        "UPDATE_SOURCE": "github_master",  # Use GitHub master branch for alpha
        "UPDATE_MODE": "auto",  # 'auto' or 'manual'
        # Add more alpha build settings here
    }
}

def get_setting(key):
    return SETTINGS[BUILD_TYPE][key]
