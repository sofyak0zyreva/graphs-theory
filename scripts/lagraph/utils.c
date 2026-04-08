#include <stdio.h>
#include <stdlib.h>
#include <suitesparse/LAGraph.h>
#include <suitesparse/GraphBLAS.h>
#include "utils.h"

LAGraph_Graph createGraph(const char *mtx_path, LAGraph_Kind kind)
{
	char msg[LAGRAPH_MSG_LEN];
	GrB_init(GrB_BLOCKING);
	LAGraph_Init(msg);

	// load matrix
	GrB_Matrix A = NULL;
	FILE *f = fopen(mtx_path, "r");
	if (f == NULL)
	{
		printf("Failed to open file: %s\n", mtx_path);
		return NULL;
	}

	LAGraph_MMRead(&A, f, msg);

	fclose(f);

	// create graph
	LAGraph_Graph G = NULL;
	LAGraph_New(&G, &A, kind, msg);
	return G;
}

LAGraph_Graph create_weighted_graph(const char *mtx_path)
{
	char msg[LAGRAPH_MSG_LEN];
	GrB_init(GrB_BLOCKING);
	LAGraph_Init(msg);

	// load matrix
	GrB_Matrix A = NULL;
	FILE *f = fopen(mtx_path, "r");
	if (f == NULL)
	{
		printf("Failed to open file: %s\n", mtx_path);
		return NULL;
	}

	int info = LAGraph_MMRead(&A, f, msg);
	if (info != GrB_SUCCESS)
	{
		printf("LAGraph_MMRead failed: %s\n", msg);
	}
	
	fclose(f);

	char name[LAGRAPH_MAX_NAME_LEN];
	GrB_Type type;
	GxB_Matrix_type(&type, A);

	int info2 = LAGraph_Matrix_TypeName(name, A, msg);
	if (info2 != GrB_SUCCESS)
	{
		printf("LAGraph_NameOfType failed: %s\n", msg);
	}
	else
	{
		printf("Matrix type: %s\n", name);
	}

	// create graph
	LAGraph_Graph G = NULL;
	LAGraph_New(&G, &A, LAGraph_ADJACENCY_DIRECTED, msg);
	return G;
}