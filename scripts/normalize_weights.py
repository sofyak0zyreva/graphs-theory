from scripts.benchmark.vars import build_path
from scripts.datasets import SSSP_DATASETS
import numpy as np

# for sssp, so that we use the same delta everywhere
def normalize_weight(input_file, output_file):
    
	rows = []
	cols = []
	vals = []

	with open(input_file, "r") as f:
		# skip comments
		header = None
		for line in f:
			if line.startswith("%"):
				continue
			else:
				header = line.strip()
				break

		# header: n_rows n_cols nnz
		n_rows, n_cols, nnz = map(int, header.split())

		# read data
		for line in f:
			parts = line.strip().split()
			if len(parts) == 3:
				i, j, w = parts
				rows.append(int(i))
				cols.append(int(j))
				vals.append(float(w))

	vals = np.array(vals)

	# max weight
	w_max = vals.max()

	# normalize
	vals_norm = vals / w_max

	# write
	with open(output_file, "w") as f:
		f.write("%%MatrixMarket matrix coordinate real general\n")
		f.write(f"{header}\n")

		for i, j, w in zip(rows, cols, vals_norm):
			f.write(f"{i} {j} {w:.8f}\n")

	print("Done. w_max =", w_max)

if __name__ == "__main__":
	for group, name in SSSP_DATASETS:
		mtx_path = build_path(name, name)
		output_path = build_path(name, name+"_norm")
		print(f"{name}")
		normalize_weight(mtx_path, output_path)
