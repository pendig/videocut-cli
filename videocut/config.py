import os
from pathlib import Path

# Base directories
HOME_DIR = Path.home()
DEFAULT_DOWNLOAD_DIR = HOME_DIR / "Downloads"
CONFIG_DIR = HOME_DIR / ".videocut"

def get_config_dir() -> Path:
    """Returns the project configuration directory."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    return CONFIG_DIR

def get_cookie_cache_path(browser: str) -> Path:
    """Returns the path for cached cookies of a specific browser."""
    return get_config_dir() / f"cookies_{browser}.txt"

def get_download_dir() -> Path:
    """Returns the default base directory for downloads."""
    return DEFAULT_DOWNLOAD_DIR

def get_platform_dir(platform: str) -> Path:
    """Returns the directory for a specific platform (e.g., youtube, instagram)."""
    platform_dir = get_download_dir() / platform
    os.makedirs(platform_dir, exist_ok=True)
    return platform_dir
