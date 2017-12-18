import os
from pathlib import Path


def road_os_path(*roadfile, level=1):
    return os.path.join(str(Path(__file__).parents[level]), *roadfile)
