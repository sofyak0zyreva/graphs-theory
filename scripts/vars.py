import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = Path("data")

OUT_DIR = Path("data/gr")
OUT_DIR.mkdir(parents=True, exist_ok=True)


