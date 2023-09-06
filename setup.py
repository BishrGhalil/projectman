import os
import shutil
from pathlib import Path

from setuptools import setup


def pre_install_func():
    source_directory = "templates"
    destination_directory = Path.home() / ".projectman" / source_directory
    os.makedirs(destination_directory, exist_ok=True)
    shutil.copytree(source_directory, destination_directory)


if __name__ == "__main__":
    setup(
        setup_requires=["setuptools"],
        pre_install_func=pre_install_func,
    )
