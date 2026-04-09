# graphs-theory

## How to get started
You need to build LAGraph + GraphBLAS localy:
```
git clone git@github.com:DrTimothyAldenDavis/GraphBLAS.git
cd GraphBLAS
make
sudo make install
```
```
git clone git@github.com:GraphBLAS/LAGraph.git
make
make test
sudo make install
```
Clone this repo (and SPLA recursively):
```
git clone git@github.com:sofyak0zyreva/graphs-theory.git
cd graphs-theory
git submodule update --init --recursive
```
Build SPLA:
```
cd external/spla
mkdir build && cd build
cmake ..   -DCMAKE_BUILD_TYPE=Release   -DSPLA_BUILD_EXAMPLES=ON   -DOPENCL_LIBRARY=/System/Library/Frameworks/OpenCL.framework   -DOPENCL_INCLUDE_DIR=/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/OpenCL.framework/Headers
make -j8
```
You're all set!
## Main pipeline
Install needed libraries:
```
# you are in graphs-theory
python3 -m venv path/to/venv
source path/to/venv/bin/activate
pip install -r requierements.txt
```
Download datasets (make sure you have enogugh disk space!):
```
python -m scripts.download_datasets
```
Additional checks: normalize weights for SSSP (w -> [0;1]), check if there are any loops or multiedges for TC:
```
python -m scripts.normalize_weights # new datasets in "name_norm.mtx"
python -m scripts.process_edges
```
Build LAGraph binaries for BFS, SSSP, PageRank, TC:
```
make
```
Benchmark: 
```
python -m scripts.benchmark.run_bfs > scripts/benchmark/results/bfs.txt
python -m scripts.benchmark.run_sssp > scripts/benchmark/results/sssp.txt
python -m scripts.benchmark.run_pr > scripts/benchmark/results/pr.txt
python -m scripts.benchmark.run_tc > scripts/benchmark/results/tc.txt

```
Save plots and tables to `output` folder:
```
python -m scripts.show_results
```
## Contacts
[sofyak0zyreva](https://github.com/sofyak0zyreva) (tg @soffque)  

## License
The product is distributed under MIT license. See [`LICENSE`](LICENSE) for details.
