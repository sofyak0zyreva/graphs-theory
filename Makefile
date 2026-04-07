CC = cc

# Пути к SuiteSparse (GraphBLAS + LAGraph)
CFLAGS = -I/usr/local/include/suitesparse
LDFLAGS = -L/usr/local/lib -lgraphblas -llagraph

# Исходники и бинарники
LAGRAPH_SRC = scripts/lagraph_bfs.c
LAGRAPH_BIN = build/lagraph_bfs

all: lagraph

lagraph: $(LAGRAPH_BIN)

$(LAGRAPH_BIN): $(LAGRAPH_SRC)
	@mkdir -p build
	$(CC) $(LAGRAPH_SRC) -o $(LAGRAPH_BIN) $(CFLAGS) $(LDFLAGS)

clean:
	rm -rf build/*