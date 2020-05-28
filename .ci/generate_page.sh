#!/bin/sh -ex

export BRANCHES="master v20.05"

mkdir -p public

passed=1

for BRANCH in $BRANCHES; do
	if ! [ -e upstream-compat-"$BRANCH".check-passed ]; then
		passed=0
		break
	fi
done

if [ "$passed" -eq 1 ]; then
	cp badges/upstream-compat-passed.svg public/upstream-compat.svg
else
	cp badges/upstream-compat-failed.svg public/upstream-compat.svg
fi
