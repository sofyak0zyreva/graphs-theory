import os
from pathlib import Path

# we will not consider the first perf result
N_ITERS = 6

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

LAGRAPH_BFS_BIN = ROOT / "build/lagraph_bfs"
SPLA_BFS_BIN = ROOT / "external/spla/build/bfs"


LAGRAPH_PR_BIN = ROOT / "build/lagraph_pr"
SPLA_PR_BIN = ROOT / "external/spla/build/pr"

LAGRAPH_SSSP_BIN = ROOT / "build/lagraph_sssp"
SPLA_SSSP_BIN = ROOT / "external/spla/build/sssp"

def build_path(group, name):
    return os.path.join(DATA_DIR, group, f"{name}.mtx")
