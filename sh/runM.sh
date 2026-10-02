set -e

Ms=(100 200 500 1000 1500 2000 2500 3000)
for M in ${Ms[@]}; do
    echo "======== M = $M ========"
    echo "Running PLBF_M"
    python src/PLBFs/PLBF_M.py --data_path data/example.csv --N 50 --k 5 --M $M
    echo ""
    echo "Running FastPLBF_M"
    python src/PLBFs/FastPLBF_M.py --data_path data/example.csv --N 50 --k 5 --M $M
    echo ""
    echo "Running FastPLBFpp_M"
    python src/PLBFs/FastPLBFpp_M.py --data_path data/example.csv --N 50 --k 5 --M $M
    echo ""
    echo "Running FastPLBFsharp_M"
    python src/PLBFs/FastPLBFsharp_M.py --data_path data/example.csv --N 50 --k 5 --M $M
    echo ""
done
