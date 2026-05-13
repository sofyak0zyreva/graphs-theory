import subprocess
from pathlib import Path
from scripts.datasets import *
from scripts.vars import *

GRAPH_CONVERT = GALOIS_ROOT / "build/tools/graph-convert/graph-convert"


def run(cmd):
    # print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def convert_mtx_to_gr_dir_weighted(mtx_file: Path):
    name = mtx_file.stem

    gr_file = OUT_DIR / f"{name}.gr"
    tgr_file = OUT_DIR / f"{name}.tgr"

    # mtx -> gr
    run([
        GRAPH_CONVERT,
        "--edgelist2gr",
        str(mtx_file),
        str(gr_file),
        "--edgeType=float32"
    ])

    # gr -> tgr
    run([
        GRAPH_CONVERT,
        "--gr2tgr",
        str(gr_file),
        str(tgr_file)
    ])

    print(f"Done: {name}")

def convert_mtx_to_gr_undir_weighted(mtx_file: Path):
    name = mtx_file.stem

    gr_file = OUT_DIR / f"{name}.gr"
    tgr_file = OUT_DIR / f"{name}.tgr"

    # mtx -> gr
    run([
        GRAPH_CONVERT,
        "--edgelist2gr",
        str(mtx_file),
        str(gr_file),
        "--edgeType=float32"
    ])

    # gr -> gr + reversed edges
    run([
        GRAPH_CONVERT,
        "--gr2sgr",
        str(gr_file),
        str(gr_file),
        "--edgeType=float32"
    ])

    # gr -> tgr
    run([
        GRAPH_CONVERT,
        "--gr2tgr",
        str(gr_file),
        str(tgr_file)
    ])

    print(f"Done: {name}")

def convert_mtx_to_gr_undir(mtx_file: Path):
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

    # gr -> gr + reversed edges
    run([
        GRAPH_CONVERT,
        "--gr2sgr",
        str(gr_file),
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

def convert_mtx_to_gr_dir(mtx_file: Path):
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


if __name__ == "__main__":
    for group, name in list(set(BFS_DATASETS + TC_DATASETS + SSSP_DATASETS)):
        mtx_files = DATA_DIR / name / (name + ".mtx")
        convert_mtx_to_gr_undir(mtx_files)
    for group, name in list(set(PAGERANK_DATASETS)):
        mtx_files = DATA_DIR / name / (name + ".mtx")
        convert_mtx_to_gr_dir(mtx_files)
    for group, name in list(set(SSSP_DATASETS)):

        mtx_files = DATA_DIR / name / (name + ".mtx")
        if (name == "pa2010" or name == "pdb1HYS"):
            convert_mtx_to_gr_undir_weighted(mtx_files)
        else: 
            convert_mtx_to_gr_dir_weighted(mtx_files)
