import subprocess
import re
import csv
from scripts.vars import *
from scripts.datasets import TC_DATASETS
from scripts.benchmark.helpers import *

GALOIS_TC = GALOIS_BIN + "triangle-counting/triangle-counting-dist"

OUTPUT_TC = OUTPUT_CSV / "tc_results.csv"


def run(graph, nproc):
    galois_bin = str(GALOIS_TC)

    cmd = [
        "mpirun",
        "-n",
        str(nproc),
        galois_bin,
        str(graph),
        "-graphTranspose=" + str(graph).replace(".gr", ".tgr"),
        "-t=" + str(THREADS),
        "-runs=" + str(RUNS),
        "--symmetricGraph",
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
    repl_nodes = re.findall(r"ReplicationFactorNodes,[^,]+,\s*([\d.]+)", out)
    if not repl_nodes:
        repl_nodes = "-"
    print(repl_nodes)
    repl_edges = re.findall(r"ReplicatonFactorEdges,[^,]+,\s*([\d.]+)", out)
    if not repl_edges:
        repl_edges = "-"
    print(repl_edges)
    constr = re.findall(r"GraphConstructTime,[^,]+,\s*([\d.]+)", out)
    if not constr:
        constr = "-"
    print(constr)
    CSREdgeSort = re.findall(r"CSREdgeSort,[^,]+,[^,]+,\s*([\d.]+)", out)
    if not CSREdgeSort:
        CSREdgeSort = "-"
    print(CSREdgeSort)
    EdgeInspectionBytesSent = re.findall(
        r"EdgeInspectionBytesSent,[^,]+,\s*([\d.]+)", out
    )
    if not EdgeInspectionBytesSent:
        EdgeInspectionBytesSent = "-"
    print(EdgeInspectionBytesSent)
    distr = re.findall(
        r"Master distribution time\s*:\s*([-+]?[\d.]+(?:e[-+]?\d+)?)", out
    )
    if not distr:
        distr = [0]
    numbers = [round(float(x) * 1000, 2) for x in distr]
    distr_final = np.mean(numbers)

    return (
        mean_rounded,
        err_rounded,
        repl_nodes[0],
        repl_edges[0],
        constr[0],
        CSREdgeSort[0],
        EdgeInspectionBytesSent[0],
        distr_final,
    )


def main():
    rows = []
    for _, name in TC_DATASETS:
        g = build_path(name)
        for n in NS:
            try:
                (
                    mean,
                    std,
                    repl_nodes,
                    repl_edges,
                    constr,
                    CSREdgeSort,
                    EdgeInspectionBytesSent,
                    distr,
                ) = run(g, n)
                if mean is None or std is None:
                    continue
                rows.append(
                    {
                        "graph": name,
                        "nodes": n,
                        "mean": mean,
                        "stderr": std,
                        "repl nodes": repl_nodes,
                        "repl edges": repl_edges,
                        "constr": constr,
                        "CSREdgeSort": CSREdgeSort,
                        "EdgeInspectionBytesSent": EdgeInspectionBytesSent,
                        "distr": distr,
                    }
                )

            except Exception as e:
                print("ERROR:", g, n, e)

    with open(OUTPUT_TC, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "graph",
                "nodes",
                "mean",
                "stderr",
                "repl nodes",
                "repl edges",
                "constr",
                "CSREdgeSort",
                "EdgeInspectionBytesSent",
                "distr",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print("Saved to", OUTPUT_TC)


if __name__ == "__main__":
    main()
