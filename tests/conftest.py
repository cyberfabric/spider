from __future__ import annotations

import sys
from pathlib import Path


def pytest_configure() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    spaider_scripts_dir = repo_root / "skills" / "spaider" / "scripts"
    sys.path.insert(0, str(spaider_scripts_dir))
