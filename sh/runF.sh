set -e

Fs=(0.5 0.2 0.1 0.05 0.02 0.01 0.005 0.001)
for F in ${Fs[@]}; do
    echo "======== F = $F ========"
    echo "Running PLBF"
    python src/PLBFs/PLBF.py --data_path data/example.csv --N 50 --k 5 --F $F
    echo ""
    echo "Running FastPLBF"
    python src/PLBFs/FastPLBF.py --data_path data/example.csv --N 50 --k 5 --F $F
    echo ""
    echo "Running FastPLBFpp"
    python src/PLBFs/FastPLBFpp.py --data_path data/example.csv --N 50 --k 5 --F $F
    echo ""
done
