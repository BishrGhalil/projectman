import os
from pathlib import Path

CONFIG_PATH = Path.home() / ".projectman"
os.makedirs(CONFIG_PATH, exist_ok=True)
