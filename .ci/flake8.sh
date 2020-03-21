#!/bin/sh -e
topdir="$(realpath "$(dirname "$0")/..")"
cd "$topdir"

flake8 $(find -name '*.py')

echo "flake8 check passed"
