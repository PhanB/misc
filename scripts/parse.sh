#!/bin/bash

if [ -z "$1" ]; then
	echo 'Usage: ./parse <xslx file to parse>'
	exit
fi

./convert.sh "$1"

#strip away directories
IFS='/' read -ra parsed <<< "$1" #convert string to array
csv=${parsed[-1]} #get file only (not directories)
mycsv=${csv::-5} #remove .xslx

directory="../csv/"
file_path="$directory$mycsv.csv"
#file_path+=".csv"

#echo "$file_path"

./get_averages.sh "$file_path"

echo "Averages are available in averages.csv"
