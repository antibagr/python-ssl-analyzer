#!/bin/bash

# Check if the input file exists
if [ ! -f "$1" ]; then
    echo "Input file not found: $1"
    exit 1
fi

# Remove output file if it already exists
if [ -f "$2" ]; then
    rm "$2"
fi

while IFS= read -r line || [ -n "$line" ]; do
    host=$(echo "$line" | cut -d: -f1)
    port=$(echo "$line" | cut -d: -f2)
    cmd="MAX_PARALLEL=100 testssl.sh --jsonfile ./results/${host////_}  --mode parallel --quiet --protocols --server-defaults --overwrite $host:$port"

    echo "$cmd" >>"$2"
done <"$1"

chmod +x "$2"
echo "commands generated in $2"
