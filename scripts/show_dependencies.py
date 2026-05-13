import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.vars import *
import math


def dep(algo, category, name):
	path = OUTPUT_CSV
	csv_path = algo + "_results.csv"
	df = pd.read_csv(path / csv_path)
	df.columns = df.columns.str.strip()

	# df.loc[df[category] == 0, category] 
	df.loc[df[category] == math.nan, category] = 0.1

	graphs = df['graph'].unique()
	num_graphs = len(graphs)

	cols = 2
	rows = math.ceil(num_graphs / cols)
	fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 6))
	axes = axes.flatten()

	for i, graph_name in enumerate(graphs):
		ax = axes[i]
		subset = df[df['graph'] == graph_name].sort_values(category)

		x = subset[category]
		y = subset['mean']

		ax.plot(x, y, marker='o', color='royalblue', linewidth=2, markersize=8)

		ax.set_xscale('log')
		ax.set_yscale('log')

		for xi, yi in zip(x, y):
			label = f"RM:{xi:.1f}\nM:{yi:.3g}"
			ax.annotate(label,
						(xi, yi),
						textcoords="offset points",
						xytext=(0, 10),
						ha='center',
						fontsize=8,
						bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))

		ax.set_title(f'Graph: {graph_name}', fontsize=14, fontweight='bold')
		ax.set_xlabel(name)
		ax.set_ylabel('Mean (log scale)')
		ax.grid(True, which="both", ls="-", alpha=0.2)  

	for j in range(i + 1, len(axes)):
		fig.delaxes(axes[j])

	plt.tight_layout()
	filename = algo + "_" + category +".png"
	plt.savefig(path / filename, dpi=300, bbox_inches="tight")
	# plt.show()


# dep("pr", 'sync', 'Sync')
# dep("pr", 'replication factor', 'Replication factor')
# dep("pr", 'reset mirror', 'Reset mirror')
# dep("pr", 'reduce send bytes', 'Reduce send bytes')

# dep("tc", 'CSREdgeSort', 'CSREdgeSort')


def dep2(algo, category, name):
	path = OUTPUT_CSV
	csv_path = algo + "_results.csv"
	df = pd.read_csv(path / csv_path)
	df.columns = df.columns.str.strip()

	# df.loc[df[category] == 0, category]
	# df.loc[df[category] == 0, category] = 0.1

	graphs = df['graph'].unique()
	num_graphs = len(graphs)

	cols = 2
	rows = math.ceil(num_graphs / cols)
	fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 6))
	axes = axes.flatten()

	for i, graph_name in enumerate(graphs):
		ax = axes[i]
		subset = df[df['graph'] == graph_name].sort_values(category)

		x = subset['nodes']
		y = subset[category]

		ax.plot(x, y, marker='o', color='royalblue', linewidth=2, markersize=8)

		ax.set_xscale('log')
		# ax.set_yscale('log')

		for xi, yi in zip(x, y):
			label = f"RM:{xi:.1f}\nM:{yi:.3g}"
			ax.annotate(label,
                            (xi, yi),
                            textcoords="offset points",
                            xytext=(0, 10),
                            ha='center',
                            fontsize=8,
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))

		ax.set_title(f'Graph: {graph_name}', fontsize=14, fontweight='bold')
		ax.set_xlabel("nodes")
		ax.set_ylabel(name)
		ax.grid(True, which="both", ls="-", alpha=0.2)

	for j in range(i + 1, len(axes)):
		fig.delaxes(axes[j])

	plt.tight_layout()
	filename = algo + "_" + category + "2.png"
	plt.savefig(path / filename, dpi=300, bbox_inches="tight")
	# plt.show()


# dep2("tc", 'EdgeInspectionBytesSent', 'EdgeInspectionBytesSent')
# dep2("sssp", 'sync', 'sync')
# dep2("sssp", 'replication factor', 'replication factor')
# dep2("tc", 'CSREdgeSort', 'CSREdgeSort')
