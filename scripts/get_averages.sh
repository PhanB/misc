#!/bin/bash

if [ -z "$1" ]; then
	echo 'Usage: ./averages.sh <csv file to find averages of>'
	exit
fi

#py excel2csv.py "$1" Gas\ Volume
#py alltech_cols.py $1 | ./transpose.sh | sed 's/ /\t/g'
tail '-n+4' "$1" > "$1.tmp" && mv "$1.tmp" "$1"; 
py "awkcols.py" "$1" "average" | ./transpose.sh | sed 's/ /,/g' > 'averages.csv'
