foo=$1
bar=${1%.*}
python ../pyCPP/parser.py $1
echo "Running test"
spim file $bar.asm
