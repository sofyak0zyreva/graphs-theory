#include <stdio.h>
#include <stdlib.h>
#include <suitesparse/LAGraph.h>
#include <suitesparse/GraphBLAS.h>

int main(int argc, char **argv)
{
	if (argc < 3)
	{
		printf("Usage: %s matrix.mtx n_iters source\n", argv[0]);
		return 1;
	}

	char msg[LAGRAPH_MSG_LEN];
	const char *mtx_path = argv[1];

	int n_iters = atoi(argv[2]);

	GrB_init(GrB_BLOCKING);
	LAGraph_Init(msg);

	// load matrix
	GrB_Matrix A = NULL;
	FILE *f = fopen(mtx_path, "r");
	if (f == NULL)
	{
		printf("Failed to open file: %s\n", mtx_path);
		return 1;
	}

	LAGraph_MMRead(&A, f, NULL);

	fclose(f);

	// create graph
	LAGraph_Graph G = NULL;
	LAGraph_New(&G, &A, LAGraph_ADJACENCY_DIRECTED, NULL);

	// required
	LAGraph_Cached_OutDegree(G, msg);
	LAGraph_Cached_AT(G, msg);

	// algo params
	GrB_Vector centrality;
	int iters;
	float damping = 0.85;
	float tol = 1e-4;
	int itermax = 100;

	for (int i = 0; i < n_iters; i++)
	{
		double t0 = LAGraph_WallClockTime();

		LAGr_PageRank(&centrality, &iters, G, damping, tol, itermax, msg);

		double t1 = LAGraph_WallClockTime();

		double elapsed_ms = (t1 - t0) * 1000.0;

		printf("iter %d: %.6f ms\n", i, elapsed_ms);

		// cleanup
		GrB_free(&centrality);
	}

	LAGraph_Delete(&G, NULL);
	GrB_free(&A);

	LAGraph_Finalize(NULL);
	GrB_finalize();

	return 0;
}