#include <stdio.h>
#include <stdlib.h>
#include <suitesparse/LAGraph.h>
#include <suitesparse/GraphBLAS.h>
#include "utils.h"

int main(int argc, char **argv)
{
	if (argc < 3)
	{
		printf("Usage: %s matrix.mtx n_iters\n", argv[0]);
		return 1;
	}

	char msg[LAGRAPH_MSG_LEN];
	const char *mtx_path = argv[1];

	int n_iters = atoi(argv[2]);

	LAGraph_Graph G = createGraph(mtx_path, LAGraph_ADJACENCY_UNDIRECTED);

	// algo params
	uint64_t ntriangles;
	LAGr_TriangleCount_Method method = LAGr_TriangleCount_Burkhardt;

	LAGraph_Cached_NSelfEdges(G, msg);
	LAGraph_Cached_OutDegree(G, msg);

	for (int i = 0; i < n_iters; i++)
	{
		double t0 = LAGraph_WallClockTime();

		int status = LAGr_TriangleCount(&ntriangles, G, &method, NULL, msg);

		double t1 = LAGraph_WallClockTime();

		if (status != GrB_SUCCESS)
		{
			printf("TC failed %d\n", status);
		}
		// printf("TC num: %llu\n", (unsigned long long)ntriangles);

		double elapsed_ms = (t1 - t0) * 1000.0;

		printf("iter %d: %.6f ms\n", i, elapsed_ms);
	}

	LAGraph_Delete(&G, msg);

	LAGraph_Finalize(msg);
	GrB_finalize();

	return 0;
}