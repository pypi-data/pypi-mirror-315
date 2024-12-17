from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent.parent.parent / "data"


def basicConfig(base_dir: Path = BASE_DIR):
    BASE_DIR = base_dir
