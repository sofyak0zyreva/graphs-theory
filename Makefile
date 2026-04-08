CC = cc

# paths (GraphBLAS + LAGraph)
CFLAGS = -I/usr/local/include/suitesparse
LDFLAGS = -L/usr/local/lib -lgraphblas -llagraph -Wl,-rpath,/usr/local/lib

LAGRAPH_UTILS = scripts/lagraph/utils.c

LAGRAPH_BFS_SRC = scripts/lagraph/lagraph_bfs.c
LAGRAPH_BFS_BIN = build/lagraph_bfs

LAGRAPH_PR_SRC = scripts/lagraph/lagraph_pr.c
LAGRAPH_PR_BIN = build/lagraph_pr

LAGRAPH_SSSP_SRC = scripts/lagraph/lagraph_sssp.c
LAGRAPH_SSSP_BIN = build/lagraph_sssp

.PHONY: all clean lagraph_bfs lagraph_pr lagraph_sssp

all: lagraph_bfs lagraph_pr lagraph_sssp

lagraph_bfs: $(LAGRAPH_BFS_BIN)

$(LAGRAPH_BFS_BIN): $(LAGRAPH_BFS_SRC)
	mkdir -p build
	$(CC) $< $(LAGRAPH_UTILS) -o $@ $(CFLAGS) $(LDFLAGS)

lagraph_pr: $(LAGRAPH_PR_BIN)

$(LAGRAPH_PR_BIN): $(LAGRAPH_PR_SRC)
	mkdir -p build
	$(CC) $< $(LAGRAPH_UTILS) -o $@ $(CFLAGS) $(LDFLAGS)

lagraph_sssp: $(LAGRAPH_SSSP_BIN)

$(LAGRAPH_SSSP_BIN): $(LAGRAPH_SSSP_SRC)
	mkdir -p build
	$(CC) $< $(LAGRAPH_UTILS) -o $@ $(CFLAGS) $(LDFLAGS)

clean:
	rm -rf build