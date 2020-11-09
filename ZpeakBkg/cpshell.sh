#!/bin/bash

read -p "Please enter source file name: " filename
read -p "Please enter the number of files which you will copy: " num

int=1

while ((int <= num))
do
    cp "${filename}" "${filename%.py*}_${int}.py"
    ((int++))
done

