foo=$1
bar=${1%.*}
cd ../pyCPP/
python parser.py ../tests/$1
cd ../tests/
echo "Running test"
spim file $bar.asm
