foo=$1
bar=${1%.*}
cd ../pyCPP/
python parser.py ../Final_tests/$1
cd ../Final_tests/
echo "Running test"
../pyCPP/optimizer $bar.asm > ${bar}o.asm
spim file ${bar}o.asm
