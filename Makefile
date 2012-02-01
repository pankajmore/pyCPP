#  ---------------------------------------------------------------
#  Makefile
#
#  Python C++ Compiler - Makefile

#  This just makes all the sample code and lets you clean up
#  intermediate/output files.
#  ---------------------------------------------------------------

#FLAGS=-annotate -ast
PYTHON=python

#compile-samples:
#		${PYTHON} c.py samples/foo.c samples/foo_lib.c ${FLAGS}

clean:
		rm -f parsetab.py parser.out *.pyc
