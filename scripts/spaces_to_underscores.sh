#!/bin/bash

#run this in the directory you wish to convert filenames from spaces to underscores

#if [ -z "$1" ]; then
#	echo "$1"
#	cd "$1"
#fi


for f in *\ *; do mv "$f" "${f// /_}"; done
