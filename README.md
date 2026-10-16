# Fast Partitioned Learned Bloom Filter

This repository contains the Python implementation for the following papers:

- Atsuki Sato and Yusuke Matsui. **"Fast Partitioned Learned Bloom Filter."** NeurIPS 2023. [[arXiv](https://arxiv.org/abs/2306.02846)]
- Atsuki Sato and Yusuke Matsui. **"Fast Construction of Partitioned Learned Bloom Filter with Theoretical Guarantees."** The VLDB Journal, 2026. [[arXiv](https://arxiv.org/abs/2410.13278)]

## Methods

This repository implements the original PLBF and three methods that accelerate its construction.

| Method | Proposed in | Construction time | Data structure compared with PLBF |
|---|---|---|---|
| PLBF | Vaidya et al., ICLR 2021 | $O(N^3 k)$ | — |
| fast PLBF | Sato and Matsui, NeurIPS 2023 | $O(N^2 k)$ | Always identical |
| fast PLBF++ | Sato and Matsui, NeurIPS 2023 | $O(N k \log N)$ | Identical under the ideal condition; bounded difference otherwise |
| fast PLBF# | Sato and Matsui, VLDB Journal 2026 | $O(N k \log k)$ | Identical under the ideal condition |

$N$ is the number of *segments* and $k$ is the number of *regions*.

- **PLBF** is the original partitioned learned Bloom filter. Its parameters are optimized by dynamic programming (DP).
- **fast PLBF** constructs exactly the same data structure as PLBF. It builds the DP table only once and reuses it, which removes redundant computation.
- **fast PLBF++** speeds up the DP using the monotone maxima algorithm. It is guaranteed to give the same data structure as PLBF when the score distribution is ideal. In the non-ideal case, its difference from PLBF is theoretically bounded.
- **fast PLBF#** speeds up the DP using the SMAWK algorithm. It is guaranteed to give the same data structure as PLBF when the score distribution is ideal.

(In the NeurIPS 2023 paper, the complexity of fast PLBF++ was $O(Nk \log N + Nk^2)$. The VLDB Journal version improves it to $O(Nk \log N)$.)

## Two Problem Settings

Every method is implemented in two variants. The variants differ only in which quantity is given as input and which one is optimized.

- **FPR-constrained** (scripts without a suffix, e.g., `FastPLBF.py`):
  you specify the target overall false positive rate `F`, and the backup Bloom filters' memory usage is minimized.
  This is the formulation used in the original PLBF paper.
- **Memory-constrained** (scripts with the `_M` suffix, e.g., `FastPLBF_M.py`):
  you specify the memory budget `M` for the backup Bloom filters, and the expected false positive rate is minimized.
  This variant makes it easy to compare methods at the same memory usage, so the experiments in our papers use it.

Choosing between these two settings does not change any of the methods above. The acceleration techniques apply in exactly the same way to both settings.

## Repository Structure

```
.
├── data/
│   └── example.csv           # example input (keys, labels, scores)
└── src/
    └── PLBFs/
        ├── PLBF.py               # PLBF          (FPR-constrained)
        ├── FastPLBF.py           # fast PLBF     (FPR-constrained)
        ├── FastPLBFpp.py         # fast PLBF++   (FPR-constrained)
        ├── FastPLBFsharp.py      # fast PLBF#    (FPR-constrained)
        ├── PLBF_M.py             # PLBF          (memory-constrained)
        ├── FastPLBF_M.py         # fast PLBF     (memory-constrained)
        ├── FastPLBFpp_M.py       # fast PLBF++   (memory-constrained)
        └── FastPLBFsharp_M.py    # fast PLBF#    (memory-constrained)
```

## Usage

### FPR-constrained setting

**Input arguments**
- `--data_path`: CSV file that contains the items, scores, and labels
- `--N`: Number of *segments*
- `--k`: Number of *regions*
- `--F`: Target overall false positive rate

**Commands**
```bash
python src/PLBFs/PLBF.py          --data_path data/example.csv --N 50 --k 5 --F 0.01
python src/PLBFs/FastPLBF.py      --data_path data/example.csv --N 50 --k 5 --F 0.01
python src/PLBFs/FastPLBFpp.py    --data_path data/example.csv --N 50 --k 5 --F 0.01
python src/PLBFs/FastPLBFsharp.py --data_path data/example.csv --N 50 --k 5 --F 0.01
```

### Memory-constrained setting

**Input arguments**
- `--data_path`: CSV file that contains the items, scores, and labels
- `--N`: Number of *segments*
- `--k`: Number of *regions*
- `--M`: Target memory usage for the backup Bloom filters

**Commands**
```bash
python src/PLBFs/PLBF_M.py          --data_path data/example.csv --N 50 --k 5 --M 1000
python src/PLBFs/FastPLBF_M.py      --data_path data/example.csv --N 50 --k 5 --M 1000
python src/PLBFs/FastPLBFpp_M.py    --data_path data/example.csv --N 50 --k 5 --M 1000
python src/PLBFs/FastPLBFsharp_M.py --data_path data/example.csv --N 50 --k 5 --M 1000
```

## Citation

If you use this code, please cite:

```bibtex
@inproceedings{sato2023fast,
  title     = {Fast Partitioned Learned Bloom Filter},
  author    = {Sato, Atsuki and Matsui, Yusuke},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year      = {2023}
}

@article{sato2026fast,
  title   = {Fast Construction of Partitioned Learned Bloom Filter with Theoretical Guarantees},
  author  = {Sato, Atsuki and Matsui, Yusuke},
  journal = {The VLDB Journal},
  year    = {2026},
  note    = {Accepted, to appear}
}
```

The original PLBF:

```bibtex
@inproceedings{vaidya2021partitioned,
  title     = {Partitioned Learned Bloom Filters},
  author    = {Vaidya, Kapil and Knorr, Eric and Mitzenmacher, Michael and Kraska, Tim},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2021}
}
```
