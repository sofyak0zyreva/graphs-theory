import subprocess
import re
import csv
import numpy as np
from pathlib import Path
from scripts.vars import *
from scripts.datasets import BFS_DATASETS
from scripts.benchmark.helpers import *

# === CONFIG ===
GALOIS_BIN = "./build/lonestar/analytics/distributed/bfs/bfs-push-dist"
GALOIS_ROOT = ROOT / "/Galois"
REPO_ROOT = ROOT / "graphs-theory"
# print(ROOT)
# print(GALOIS_ROOT)

THREADS = 1
RUNS = 10
HOSTS = "localhost"

NS = [1, 2, 4, 8]   

OUTPUT_CSV = "/Users/sofyakozyreva/graphs-theory/scripts/benchmark/results/bfs_results.csv"
# OUTPUT_CSV.parent.mkdir(exist_ok=True)


def run_bfs(graph, nproc):
    galois_bin = str(GALOIS_BIN)
    cmd = [
        "mpirun",
        "-n", str(nproc),
        galois_bin,
        str(graph),
        "-graphTranspose=" + str(graph).replace(".gr", ".tgr"),
        "-t="+str(THREADS),
        "-runs="+str(10),
        "-startNode="+str(1000)
    ]
    # print(cmd)
    print("RUN:", " ".join(cmd))
    galois_root = str(GALOIS_ROOT)

    p = subprocess.run(cmd, cwd="/Users/sofyakozyreva/Galois/",
                       capture_output=True, text=True)

    out = p.stdout + p.stderr
    print(out)

    # extract TimerTotal
    match = re.findall(r"run:\s*([0-9.]+)", out)
    # print("match")
    print(match)

    if not match:
        return None

    times = list(map(float, match))
    result = times[1:]

    print(len(result))
    mean = np.mean(result)
    std = np.std(result, ddof=1)
    err_rounded = round_error(std)
    mean_rounded = match_decimal_places(mean, err_rounded)
    repl = re.findall(r"ReplicationFactor,[^,]+,\s*([\d.]+)", out)
    if not repl:
        repl = "-"
    print(repl)
    
    return mean_rounded, err_rounded, repl[0]


def build_path(name):
    return os.path.join("/Users/sofyakozyreva/graphs-theory/data/gr/", f"{name}.gr")


def main():
    graphs = sorted(OUT_DIR.glob("*.gr"))

    rows = []

    # for g in graphs:
    for _, name in BFS_DATASETS:
        g = build_path(name)
        for n in NS:
            try:
                mean, std, repl = run_bfs(g, n)
                if mean is None or std is None:
                    continue
                # print(t)

                rows.append({
                    "graph": name,
                    "nodes": n,
                    "mean": mean,
                    "stderr": std,
                    "replication factor": repl
                })

            except Exception as e:
                print("ERROR:", g, n, e)

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["graph", "nodes", "mean", "stderr", "replication factor"])
        writer.writeheader()
        writer.writerows(rows)

    print("Saved to", OUTPUT_CSV)


if __name__ == "__main__":
    main()
