# graphs are sorted by number of edges (ascending)

# unweighted undirected graphs with 1 strongly connected component,
# pairs of approximately the same number of edges, one with degree < 10 (first) and the other with > 15 (second)
# sorted by number of edges (ascending), range is ~1.1M-16M
BFS_DATASETS = [
    ("DIMACS10", "citationCiteseer"),
    ("DIMACS10", "vsp_msc10848_300sep_100in_1Kout"),
    ("DIMACS10", "belgium_osm"),
    ("DIMACS10", "m14b"),
    ("DIMACS10", "delaunay_n21"),
    ("DIMACS10", "kron_g500-logn17"),
    ("DIMACS10", "adaptive"),
    ("DIMACS10", "coPapersCiteseer"),
    ("SNAP", "com-Orkut"),  # a 117M edges and high avg vertex degree (76)
]

# weighted directed and undirected graphs with 1 strongly connected component,
# pairs of approximately the same number of edges, one with degree < 10 (first) and the other with > 15 (second)
# sorted by number of edges (ascending), range is ~2M-108M
SSSP_DATASETS = [
    ("DIMACS10", "pa2010"),
    ("Williams", "pdb1HYS"),
    ("GAP", "GAP-road"),
    ("vanHeukelum", "cage14"),
    ("vanHeukelum", "cage15"),  # a 100M edges and high avg vertex degree (19)
]

# unweighted directed graphs with 20k - 68.9M edges
PAGERANK_DATASETS = [
    ("SNAP", "p2p-Gnutella08"),
    ("SNAP", "p2p-Gnutella31"),
    ("SNAP", "soc-Epinions1"),
    ("SNAP", "soc-Slashdot0811"),
    ("SNAP", "amazon0302"),
    ("SNAP", "web-BerkStan"),
    ("SNAP", "soc-Pokec"),
    ("SNAP", "soc-LiveJournal1"),
]

# unweighted undirected graphs with 25k - 28.5M edges
TC_DATASETS = [
    ("DIMACS10", "delaunay_n13"),
    ("Gleich", "usroads"),
    ("DIMACS10", "fe_rotor"),
    ("SNAP", "roadNet-CA"),
    ("DIMACS10", "italy_osm"),
    ("SNAP", "as-Skitter"),
    ("DIMACS10", "road_usa"),
]


def collect_all_datasets():
    all_sets = BFS_DATASETS + PAGERANK_DATASETS + TC_DATASETS + SSSP_DATASETS
    return list(set(all_sets))
