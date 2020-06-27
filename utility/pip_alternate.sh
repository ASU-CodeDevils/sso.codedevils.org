#!/usr/bin/env bash

input="requirements.txt"
while IFS= read -r line
do
  pip install "$line"
done < "$input"