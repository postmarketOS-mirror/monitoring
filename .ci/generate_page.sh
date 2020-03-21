#!/bin/sh -ex

mkdir -p public

if [ -e .upstream-compat.check-passed ]; then
	cp badges/upstream-compat-passed.svg public/upstream-compat.svg
else
	cp badges/upstream-compat-failed.svg public/upstream-compat.svg
fi
