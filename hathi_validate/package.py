"""Package related stuff."""

import os
from typing import Iterator


def get_dirs(root: str) -> Iterator[str]:
    """Iterate over subdirectories."""
    for item in os.scandir(root):
        if item.is_dir():
            yield item.path
