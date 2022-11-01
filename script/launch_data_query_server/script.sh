#!/bin/bash

env_path="/opt/anaconda3/bin/activate pytorch"
# shellcheck disable=SC2034
code_path="/home/Documents/code/SecureDatabase"
# shellcheck disable=SC2010
str=`ls ./ | grep "^launch"`

for file in $str;
do
	# shellcheck disable=SC1090
	source $env_path
	python "$file" &
done
