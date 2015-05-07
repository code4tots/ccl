#!/bin/bash

if [ "$1" = "clean" ] || [ "$1" = "c" ]; then
	rm -rf *.tokens CclLexer.py CclListener.py CclParser.py __pycache__
elif [ "$1" = "antlr" ] || [ "$1" = "a" ]; then
	java -jar /usr/local/lib/antlr-4.5-complete.jar -Dlanguage=Python3 Ccl.g4
elif [ "$1" = "build" ] || [ "$1" = "b" ]; then
	TMP=$(cat)
	./x antlr && echo $TMP | python3 ccl.py
else
	echo "Unrecognized command '$1'"
	exit 1
fi
