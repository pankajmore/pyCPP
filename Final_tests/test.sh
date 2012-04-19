foo=$1
bar=${1%.*}
cd ../pyCPP/
python parser.py ../Final_tests/$1
cd ../Final_tests/
echo "Running test"
spim file $bar.asm
