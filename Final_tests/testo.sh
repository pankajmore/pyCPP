foo=$1
bar=${1%.*}
cd ../pyCPP/
python ./parser.py ../Final_tests/$1
echo "Running test"
cd ../Final_tests/
../pyCPP/optimizer $bar.asm > ${bar}o.asm
spim file ${bar}o.asm

