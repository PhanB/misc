#!/bin/bash

csv_dir="../csv"

if [ -z "$1" ]; then
	echo 'Usage: ./convert.sh <xlsx file to convert>'
	exit
fi

WORKSHEET_NAME="Gas Volume"
py excel2csv.py "$1" "${WORKSHEET_NAME}"
IFS='/' read -ra parsed <<< "$1" #Convert string to array
my_csv=${csv_dir}"/"${parsed[-1]}
csv_path=${my_csv::-5}
#echo ${csv_path}

sed 's/\"//g' "${csv_path}.csv" > "${csv_path}.csv.$$" && mv "${csv_path}.csv.$$" "${csv_path}.csv"
