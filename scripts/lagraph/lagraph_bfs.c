#include <stdio.h>
#include <stdlib.h>
#include <suitesparse/LAGraph.h>
#include <suitesparse/GraphBLAS.h>
#include "utils.h"

int main(int argc, char **argv)
{
	if (argc < 4)
	{
		printf("Usage: %s matrix.mtx n_iters source\n", argv[0]);
		return 1;
	}

	char msg[LAGRAPH_MSG_LEN];
	const char *mtx_path = argv[1];

	int n_iters = atoi(argv[2]);
	GrB_Index src = atoi(argv[3]);

	LAGraph_Graph G = createGraph(mtx_path, LAGraph_ADJACENCY_DIRECTED);

	// required for better performance
	LAGraph_Cached_OutDegree(G, msg);
	LAGraph_Cached_AT(G, msg);

	// algo params
	GrB_Vector level;
	GrB_Index n;
	GrB_Matrix_nrows(&n, G->A); 
	GrB_Vector_new(&level, GrB_INT32, n);

	GrB_Vector parent = NULL;

	for (int i = 0; i < n_iters; i++)
	{
		double t0 = LAGraph_WallClockTime();

		int status = LAGr_BreadthFirstSearch(&level, &parent, G, src, NULL);

		double t1 = LAGraph_WallClockTime();

		if (status != GrB_SUCCESS) {
			printf("BFS failed\n");
		}

		double elapsed_ms = (t1 - t0) * 1000.0;

		printf("iter %d: %.6f ms\n", i, elapsed_ms);

		// cleanup
		GrB_free(&level);
		GrB_free(&parent);
	}

	LAGraph_Delete(&G, msg);

	LAGraph_Finalize(msg);
	GrB_finalize();

	return 0;
}