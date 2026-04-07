# graphs are sorted by number of edges (ascending)

# unweighted directed and undirected graphs with 25k - 68.9M edges
BFS_DATASETS = [
    ("DIMACS10", "delaunay_n13"),
    ("SNAP", "email-Enron"),
    ("SNAP", "soc-Epinions1"),
    ("SNAP", "soc-Slashdot0811"),
    ("SNAP", "roadNet-CA"),
    ("SNAP", "as-Skitter"),
    ("SNAP", "soc-Pokec"),
    ("SNAP", "soc-LiveJournal1")
]

# weighted directed and undirected graphs with 34k - 27M edges
SSSP_DATASETS = [
    ("SNAP", "soc-sign-bitcoin-otc"),
    ("SNAP", "wiki-RfA"),
    ("SNAP", "soc-sign-Slashdot090221"),
    ("SNAP", "soc-sign-epinions"),
    ("vanHeukelum", "cage12"),
    ("vanHeukelum", "cage13"),
    ("Belcastro", "mouse_gene"),
    ("vanHeukelum", "cage14"),
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

# unweighted undirected graphs with 25k 28.5M edges
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
    all_sets = (
        BFS_DATASETS +
        PAGERANK_DATASETS +
        TC_DATASETS +
        SSSP_DATASETS
    )
    return list(set(all_sets))
