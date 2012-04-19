foo=$1
bar=${1%.*}
python ./parser.py $1
echo "Running test"
./optimizer $bar.asm > ${bar}o.asm
spim file ${bar}o.asm

