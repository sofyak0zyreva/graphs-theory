import subprocess
from pathlib import Path
from scripts.datasets import collect_all_datasets
from scripts.vars import *

GRAPH_CONVERT = "/Users/sofyakozyreva//Galois/build/tools/graph-convert/graph-convert"


def run(cmd):
    # print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def convert_mtx_to_gr(mtx_file: Path):
    name = mtx_file.stem

    gr_file = OUT_DIR / f"{name}.gr"
    tgr_file = OUT_DIR / f"{name}.tgr"

    # mtx -> gr
    run([
        GRAPH_CONVERT,
        "--edgelist2gr",
        str(mtx_file),
        str(gr_file)
    ])

    # gr -> tgr
    run([
        GRAPH_CONVERT,
        "--gr2tgr",
        str(gr_file),
        str(tgr_file)
    ])

    print(f"Done: {name}")


def main(name):
    mtx_files = DATA_DIR / name / (name + ".mtx")
    print(mtx_files)

    # print(f"Found {len(mtx_files)} graphs")

    # for f in mtx_files:
    convert_mtx_to_gr(mtx_files)


if __name__ == "__main__":
    for group, name in collect_all_datasets():
        main(name)
