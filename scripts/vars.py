import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = Path("data")

OUT_DIR = Path("data/gr")
OUT_DIR.mkdir(parents=True, exist_ok=True)

THREADS = 1
RUNS = 30

NS = [1, 2, 4, 8]

REPO_ROOT = ROOT / "graphs-theory"

OUTPUT_CSV = REPO_ROOT / "scripts/benchmark/results/"
GALOIS_BIN = "./build/lonestar/analytics/distributed/"
GALOIS_ROOT = ROOT / "Galois"


def build_path(name):
    return os.path.join(REPO_ROOT / "data/gr", f"{name}.gr")
