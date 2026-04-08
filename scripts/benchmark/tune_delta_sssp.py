import subprocess
from scripts.datasets import SSSP_DATASETS
from scripts.benchmark.vars import *

SOURCE = 0

DELTA = [1, 0.5, 0.1, 0.05, 0.01]

N_ITERS = 3


def run_lagraph(mtx_path, delta):
    cmd = [LAGRAPH_SSSP_BIN, mtx_path, str(N_ITERS), str(SOURCE), str(delta)]
    return subprocess.run(cmd, capture_output=True, text=True)


def run_with_diff_deltas():
    group, name = SSSP_DATASETS[0]
    mtx_path = build_path(name, name + "_norm")
    print(mtx_path)

    for delta in DELTA:
        print("\n==============================")
        print(f"Dataset: {group}/{name}")
        print(f"Delta: {delta}")
        print("==============================")

        if not os.path.exists(mtx_path):
            print(f"[SKIP] {mtx_path} not found")
            continue

        print("\n--- LAGraph ---")
        res1 = run_lagraph(mtx_path, delta)
        print(res1.stdout)
        if res1.stderr:
            print("[STDERR]")
            print(res1.stderr)


if __name__ == "__main__":
    run_with_diff_deltas()
