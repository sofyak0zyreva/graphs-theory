import re
import numpy as np  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore
from scripts.benchmark.vars import *


def significant_round(x, sig=1):
    """Round to significant digits"""
    if x == 0:
        return 0
    return round(x, sig - int(np.floor(np.log10(abs(x)))) - 1)


def round_error(err):
    """Round error to 1 significant digit, or 2 if first digit is 1"""
    if err == 0:
        return 0

    first_digit = int(str(abs(err)).replace(".", "").lstrip("0")[0])

    sig_digits = 2 if first_digit == 1 else 1
    return significant_round(err, sig_digits)


def match_decimal_places(mean, err):
    """Round mean to same decimal precision as error"""
    err_str = f"{err:.10f}".rstrip("0")
    if "." in err_str:
        decimals = len(err_str.split(".")[1])
    else:
        decimals = 0

    return round(mean, decimals)


def parse_lagraph(section):
    values = []
    for line in section.splitlines():
        m = re.search(r"iter\s+\d+:\s+([\d\.]+)", line)
        if m:
            values.append(float(m.group(1)))

    # remove iter 0
    return values[1:]


def parse_spla_gpu(section):
    gpu_match = re.search(r"gpu\(ms\):\s*(.*)", section)
    if not gpu_match:
        return []

    values = gpu_match.group(1)
    values = [float(x) for x in values.split(",") if x.strip()]

    # remove first value
    return values[1:]


def parse_spla_stats(section):
    deg_match = re.search(
        r"deg:\s*min\s*[\d\.]+,\s*max\s*[\d\.]+,\s*avg\s*([\d\.]+)", section
    )
    edges_match = re.search(r"Data:\s*([\d]+)\s*directed edges", section)

    avg_deg = float(deg_match.group(1)) if deg_match else None
    edges = int(edges_match.group(1)) if edges_match else None

    return avg_deg, edges


def extract_datasets(text):
    datasets = re.split(r"={10,}\s*Dataset:", text)
    results = []

    for block in datasets[1:]:
        name_match = re.match(r"\s*([^\n]+)", block)
        dataset_name = name_match.group(1).strip() if name_match else "Unknown"

        lagraph_section = re.search(r"--- LAGraph ---([\s\S]*?)--- Spla ---", block)
        spla_section = re.search(r"--- Spla ---([\s\S]*)", block)

        lagraph_values = (
            parse_lagraph(lagraph_section.group(1)) if lagraph_section else []
        )
        spla_gpu_values = parse_spla_gpu(spla_section.group(1)) if spla_section else []
        avg_deg, edges = (
            parse_spla_stats(spla_section.group(1)) if spla_section else (None, None)
        )

        results.append(
            {
                "name": dataset_name,
                "lagraph": lagraph_values,
                "spla": spla_gpu_values,
                "avg_deg": avg_deg,
                "edges": edges,
            }
        )

    return results


def compute_stats(values):
    mean = np.mean(values)
    std = np.std(values, ddof=1)
    return mean, std


def process_stats(values):
    mean, std = compute_stats(values)

    err_rounded = round_error(std)
    mean_rounded = match_decimal_places(mean, err_rounded)

    return mean_rounded, err_rounded


def make_table(dataset):
    lag_mean, _ = process_stats(dataset["lagraph"])
    spl_mean, _ = process_stats(dataset["spla"])

    df = pd.DataFrame(
        {
            "Method": ["LAGraph", "Spla"],
            "Time (ms)": [lag_mean, spl_mean],
            "Avg degree": [dataset["avg_deg"], dataset["avg_deg"]],
            "Edges": [dataset["edges"], dataset["edges"]],
        }
    )

    return df


def parse_algorithm_name(text):
    m = re.search(r"Algorithm:\s*(.+)", text)
    return m.group(1).strip() if m else "Unknown"


def plot_file(datasets, algo_name, save_dir):
    import os

    names = []
    lag_means = []
    spl_means = []

    for ds in datasets:
        lag_mean, _ = process_stats(ds["lagraph"])
        spl_mean, _ = process_stats(ds["spla"])

        short_name = ds["name"].split("/")[-1]

        names.append(short_name)
        lag_means.append(lag_mean)
        spl_means.append(spl_mean)

    x = np.arange(len(names))
    width = 0.35

    plt.figure(figsize=(12, 6))

    bars1 = plt.bar(x - width / 2, lag_means, width, label="LAGraph")
    bars2 = plt.bar(x + width / 2, spl_means, width, label="Spla")

    # --- подписи над столбиками ---
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.2f}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    add_labels(bars1)
    add_labels(bars2)

    plt.xticks(x, names, rotation=30, ha="right")
    plt.ylabel("Time (ms)")
    plt.title(algo_name)
    plt.legend()

    plt.tight_layout()

    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, f"{algo_name}.png")
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close()


def save_tables(datasets, algo_name, save_dir):
    import os

    os.makedirs(save_dir, exist_ok=True)

    rows = []

    for ds in datasets:
        lag_mean, lag_err = process_stats(ds["lagraph"])
        spl_mean, spl_err = process_stats(ds["spla"])

        graph_name = ds["name"].split("/")[-1]

        rows.append(
            {
                "Graph": graph_name,
                "Method": "LAGraph",
                "Time (ms)": lag_mean,
                "Avg degree": ds["avg_deg"],
                "Edges": ds["edges"],
            }
        )

        rows.append(
            {
                "Graph": graph_name,
                "Method": "Spla",
                "Time (ms)": spl_mean,
                "Avg degree": ds["avg_deg"],
                "Edges": ds["edges"],
            }
        )

    df = pd.DataFrame(rows)

    filepath = os.path.join(save_dir, f"{algo_name}.csv")
    df.to_csv(filepath, index=False)


def process_file(filepath, save_dir):
    with open(filepath, "r") as f:
        text = f.read()

    algo_name = parse_algorithm_name(text)
    datasets = extract_datasets(text)

    plot_file(datasets, algo_name, save_dir)

    save_tables(datasets, algo_name, save_dir)


def save_table_as_png(df, output_path):
    fig, ax = plt.subplots(figsize=(12, len(df) * 0.5 + 2))
    ax.axis("off")

    table = ax.table(
        cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    save_dir = os.path.join(ROOT, "output")
    names = ["bfs", "pr", "sssp", "tc"]
    for name in names:
        filepath = os.path.join(ROOT, "scripts/benchmark/results/" + f"{name}.txt")
        process_file(filepath, save_dir)
    folder_names = ["BFS", "PAGERANK", "SSSP", "TRIANGLE COUNT"]
    for folder_name in folder_names:
        read_dir = os.path.join(ROOT, "output/" + f"{folder_name}.csv")
        df = pd.read_csv(read_dir)
        print(df.to_string(index=False))
        print("\n")
        write_dir = os.path.join(ROOT, "output/" + f"{folder_name}_table.png")
        save_table_as_png(df, write_dir)
