python ../pyCPP/parser.py $1
echo "Running test"
spim file $1.asm
