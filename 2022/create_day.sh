#!/bin/bash

day=${1}

if [ -d day${day} ]; then
	echo "Directory day${day} already exits";
	exit 1
fi

mkdir day${day}
cp template/solution.py day${day}
touch day${day}/{test_,}input.dat

# TODO: Mainly developing on MacOS, if running on Linux (WSL or native), check
# OS and have if/else to use GNU or BSD sed.
sed -i '' "s/DAYNUMBER/${day}/g" day${day}/solution.py
