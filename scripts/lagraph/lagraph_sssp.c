#include <stdio.h>
#include <stdlib.h>
#include <suitesparse/LAGraph.h>
#include <suitesparse/GraphBLAS.h>
#include "utils.h"

int main(int argc, char **argv)
{
	if (argc < 5)
	{
		printf("Usage: %s matrix.mtx n_iters source\n", argv[0]);
		return 1;
	}

	char msg[LAGRAPH_MSG_LEN];
	const char *mtx_path = argv[1];

	int n_iters = atoi(argv[2]);
	GrB_Index src = atoi(argv[3]);
	float delta = atoi(argv[4]);

	LAGraph_Graph G = createGraph(mtx_path);

	// required for better performance
	LAGraph_Cached_EMin(G, msg);

	// algo params
	GrB_Vector path_length;
	GrB_Index n;
	GrB_Matrix_nrows(&n, G->A);
	GrB_Vector_new(&path_length, GrB_FP64, n);

	GrB_Scalar Delta;
	GrB_Scalar_new(&Delta, GrB_FP64);
	GrB_Scalar_setElement_FP64(Delta, delta);

	for (int i = 0; i < n_iters; i++)
	{
		double t0 = LAGraph_WallClockTime();

		int status = LAGr_SingleSourceShortestPath(&path_length, G, src, Delta, msg);

		double t1 = LAGraph_WallClockTime();

		if (status != GrB_SUCCESS)
		{
			printf("SSSP failed\n");
		}

		double elapsed_ms = (t1 - t0) * 1000.0;

		printf("iter %d: %.6f ms\n", i, elapsed_ms);

		// cleanup
		// GrB_free(&level);
		// GrB_free(&parent);
	}

	LAGraph_Delete(&G, NULL);
	// GrB_free(&A);

	LAGraph_Finalize(NULL);
	GrB_finalize();

	return 0;
}