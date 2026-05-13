import subprocess
import re
import csv
from scripts.vars import *
from scripts.datasets import PAGERANK_DATASETS
from scripts.benchmark.helpers import *

GALOIS_PR = GALOIS_BIN + "pagerank/pagerank-pull-dist"

OUTPUT_PR = OUTPUT_CSV / "pr_pull_results.csv"


def run(graph, nproc):
    galois_bin = str(GALOIS_PR)
    cmd = [
        "mpirun",
        "-n",
        str(nproc),
        galois_bin,
        str(graph),
        "-graphTranspose=" + str(graph).replace(".gr", ".tgr"),
        "-t=" + str(THREADS),
        "-runs=" + str(RUNS),
    ]
    # print(cmd)
    print("RUN:", " ".join(cmd))
    galois_root = str(GALOIS_ROOT)

    p = subprocess.run(cmd, cwd=galois_root, capture_output=True, text=True)

    out = p.stdout + p.stderr
    print(out)

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
    # print(repl)
    constr = re.findall(r"GraphConstructTime,[^,]+,\s*([\d.]+)", out)
    if not constr:
        constr = "-"
    print(constr)
    reduce_send_bytes = re.findall(
        r"ReduceSendBytes_PageRank_\d,[^,]+,\s*([\d.]+)", out
    )
    if not reduce_send_bytes:
        reduce_send_bytes = [0]
    reduce_send_bytes_final = np.mean(list(map(float, reduce_send_bytes)))
    sync = re.findall(r"Sync_PageRank_\d,[^,]+,\s*([\d.]+)", out)
    sync_final = np.mean(list(map(float, sync)))
    if not sync:
        sync = [0]
    distr = re.findall(
        r"Master distribution time\s*:\s*([-+]?[\d.]+(?:e[-+]?\d+)?)", out
    )
    if not distr:
        distr = [0]
    # print(reduce_send_bytes)
    # print(sync)
    numbers = [round(float(x) * 1000, 2) for x in distr]
    # print(numbers)
    distr_final = np.mean(numbers)
    mirr = re.findall(r"RESET:MIRRORS_\d,[^,]+,[^,]+,\s*([\d.]+)", out)
    if not mirr:
        mirr = [0]
    mirr_final = np.mean(list(map(float, mirr)))

    return (
        mean_rounded,
        err_rounded,
        repl[0],
        reduce_send_bytes_final,
        sync_final,
        distr_final,
        constr[0],
        mirr_final,
    )


def main():
    # graphs = sorted(OUT_DIR.glob("*.gr"))
    rows = []
    # for g in graphs:
    for _, name in PAGERANK_DATASETS:
        g = build_path(name)
        for n in NS:
            try:
                (
                    mean,
                    std,
                    repl,
                    reduce_send_bytes,
                    sync,
                    distr,
                    constr,
                    reset_mirror,
                ) = run(g, n)
                if mean is None or std is None:
                    continue
                # print(t)
                rows.append(
                    {
                        "graph": name,
                        "nodes": n,
                        "mean": mean,
                        "stderr": std,
                        "replication factor": repl,
                        "reduce send bytes": reduce_send_bytes,
                        "sync": sync,
                        "distr": distr,
                        "constr": constr,
                        "reset mirror": reset_mirror,
                    }
                )

            except Exception as e:
                print("ERROR:", g, n, e)

    with open(OUTPUT_PR, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "graph",
                "nodes",
                "mean",
                "stderr",
                "replication factor",
                "reduce send bytes",
                "sync",
                "distr",
                "constr",
                "reset mirror",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print("Saved to", OUTPUT_PR)


if __name__ == "__main__":
    main()
