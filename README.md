# Fast Partitioned Learned Bloom Filter

The Python files contain the implementation of PLBF, FastPLBF, FastPLBF++.

**Input arguments**
- `--data_path`: Csv file contains the items, scores, and labels
- `--N`: Number of *segments*
- `--k`: Number of *regions*
- `--F`: Target overall false positive rate

**Commands**
- run the PLBF: `python src/PLBF.py --data_path data/example.csv --N 50 --k 5 --F 0.01`
- run the FastPLBF: `python src/FastPLBF.py --data_path data/example.csv --N 50 --k 5 --F 0.01`
- run the FastPLBF++: `python src/FastPLBFpp.py --data_path data/example.csv --N 50 --k 5 --F 0.01`

