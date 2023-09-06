from pathlib import Path
import os

CONFIG_PATH = Path.home() / ".projectman"
os.makedirs(CONFIG_PATH, exist_ok=True)
