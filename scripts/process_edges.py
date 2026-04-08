from scripts.datasets import TC_DATASETS
from scripts.benchmark.vars import build_path

# for tc, so that there are no parallels edges and loops
def has_loops_or_multiedges(file_path):
	edges = set()

	with open(file_path, 'r') as f:
		for line in f:
			# skip comments
			if line.startswith('%'):
				continue

			parts = line.strip().split()

			# skip metadata
			if len(parts) == 3 and parts[0].isdigit():
				continue

			if len(parts) < 2:
				continue

			u, v = int(parts[0]), int(parts[1])
			print(f"u: {u}, v: {v}")

			# loop check
			if u == v:
				return True

			edge = (u, v)
			edge = tuple(sorted(edge))

			# check multiedges
			if edge in edges:
				return True

			edges.add(edge)

	return False

if __name__ == "__main__":
	for group, name in TC_DATASETS:
		mtx_path = build_path(name, name)
		print(f"{name}")
		if (has_loops_or_multiedges(mtx_path)):
			print("Found loops or multiedges")
		else:
			print("No loops or multiedges found!")
			
		
