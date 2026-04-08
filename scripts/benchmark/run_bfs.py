import subprocess
from scripts.datasets import BFS_DATASETS
from scripts.benchmark.vars import *

SOURCE = 0


def run_lagraph(mtx_path):
    cmd = [LAGRAPH_BFS_BIN, mtx_path, str(N_ITERS), str(SOURCE)]
    return subprocess.run(cmd, capture_output=True, text=True)


def run_spla(mtx_path):
    cmd = [
        SPLA_BFS_BIN,
        f"--mtxpath={mtx_path}",
        f"--niters={N_ITERS}",
        f"--source={SOURCE}",
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def run_all():
    print(f"Algorithm: BFS")
    for group, name in BFS_DATASETS:
        mtx_path = build_path(name, name)

        print("\n==============================")
        print(f"Dataset: {group}/{name}")
        print("==============================")

        if not os.path.exists(mtx_path):
            print(f"[SKIP] {mtx_path} not found")
            continue

        # LAGraph
        print("\n--- LAGraph ---")
        res1 = run_lagraph(mtx_path)
        print(res1.stdout)
        if res1.stderr:
            print("[STDERR]")
            print(res1.stderr)

        # SPLA
        print("\n--- Spla ---")
        res2 = run_spla(mtx_path)
        print(res2.stdout)
        if res2.stderr:
            print("[STDERR]")
            print(res2.stderr)


if __name__ == "__main__":
    run_all()
