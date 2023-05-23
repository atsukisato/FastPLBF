# Fast Partitioned Learned Bloom Filter

The Python files contain the implementation of PLBF, FastPLBF, FastPLBF++.

## Methods to minimize the memory usage under the condition of expected false positive rate.

**Input arguments**
- `--data_path`: Csv file contains the items, scores, and labels
- `--N`: Number of *segments*
- `--k`: Number of *regions*
- `--F`: Target overall false positive rate

**Commands**
- run the PLBF: `python src/PLBFs/PLBF.py --data_path data/example.csv --N 50 --k 5 --F 0.01`
- run the FastPLBF: `python src/PLBFs/FastPLBF.py --data_path data/example.csv --N 50 --k 5 --F 0.01`
- run the FastPLBF++: `python src/PLBFs/FastPLBFpp.py --data_path data/example.csv --N 50 --k 5 --F 0.01`

## Methods to minimize the expected false positive rate under the condition of memory usage.

**Input arguments**
- `--data_path`: Csv file contains the items, scores, and labels
- `--N`: Number of *segments*
- `--k`: Number of *regions*
- `--M`: Target memory usage for backup Bloom filters

**Commands**
- run the PLBF_M: `python src/PLBFs/PLBF_M.py --data_path data/example.csv --N 50 --k 5 --M 2043`
- run the FastPLBF_M: `python src/PLBFs/FastPLBF_M.py --data_path data/example.csv --N 50 --k 5 --M 2043`
- run the FastPLBF++_M: `python src/PLBFs/FastPLBFpp_M.py --data_path data/example.csv --N 50 --k 5 --M 2043`
