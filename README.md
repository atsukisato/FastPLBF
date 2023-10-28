# Fast Partitioned Learned Bloom Filter

This repository contains python implementation for our paper "[Fast Partitioned Learned Bloom Filter](https://arxiv.org/abs/2306.02846)" (NeurIPS 2023).
Three methods (PLBF, fast PLBF, and fast PLBF++) are implemented in two different frameworks: one was designed in the PLBF paper, and the other is our modified version.

## Abstract

A Bloom filter is a memory-efficient data structure for approximate membership queries used in numerous fields of computer science. Recently, learned Bloom filters that achieve better memory efficiency using machine learning models have attracted attention. One such filter, the partitioned learned Bloom filter (PLBF), achieves excellent memory efficiency. However, PLBF requires a $O(N^3 k)$ time complexity to construct the data structure, where $N$ and $k$ are the hyperparameters of PLBF. One can improve memory efficiency by increasing $N$, but the construction time becomes extremely long. Thus, we propose two methods that can reduce the construction time while maintaining the memory efficiency of PLBF. First, we propose fast PLBF, which can construct the same data structure as PLBF with a smaller time complexity $O(N^2 k)$. Second, we propose fast PLBF++, which can construct the data structure with even smaller time complexity $O(N k \log N + Nk^2)$. Fast PLBF++ does not necessarily construct the same data structure as PLBF. Still, it is almost as memory efficient as PLBF, and it is proved that fast PLBF++ has the same data structure as PLBF when the distribution satisfies a certain constraint. Our experimental results from real-world datasets show that (i) fast PLBF and fast PLBF++ can construct the data structure up to 233 and 761 times faster than PLBF, (ii) fast PLBF can achieve the same memory efficiency as PLBF, and (iii) fast PLBF++ can achieve almost the same memory efficiency as PLBF.

## Framework in the PLBF paper

This framework is designed to minimize the memory usage under the condition of expected false positive rate.

**Input arguments**
- `--data_path`: Csv file contains the items, scores, and labels
- `--N`: Number of *segments*
- `--k`: Number of *regions*
- `--F`: Target overall false positive rate

**Commands**
- run the PLBF: `python src/PLBFs/PLBF.py --data_path data/example.csv --N 50 --k 5 --F 0.01`
- run the FastPLBF: `python src/PLBFs/FastPLBF.py --data_path data/example.csv --N 50 --k 5 --F 0.01`
- run the FastPLBF++: `python src/PLBFs/FastPLBFpp.py --data_path data/example.csv --N 50 --k 5 --F 0.01`

## Framework in our paper

This framework is designed to minimize the expected false positive rate under the condition of memory usage.

**Input arguments**
- `--data_path`: Csv file contains the items, scores, and labels
- `--N`: Number of *segments*
- `--k`: Number of *regions*
- `--M`: Target memory usage for backup Bloom filters

**Commands**
- run the PLBF_M: `python src/PLBFs/PLBF_M.py --data_path data/example.csv --N 50 --k 5 --M 1000`
- run the FastPLBF_M: `python src/PLBFs/FastPLBF_M.py --data_path data/example.csv --N 50 --k 5 --M 1000`
- run the FastPLBF++_M: `python src/PLBFs/FastPLBFpp_M.py --data_path data/example.csv --N 50 --k 5 --M 1000`
