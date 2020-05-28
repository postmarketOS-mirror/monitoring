#!/bin/sh -ex

wget "https://gitlab.com/postmarketOS/ci-common/-/raw/master/install_pmbootstrap.sh"
sh ./install_pmbootstrap.sh pytest
ln -s /tmp/pmbootstrap/pmb .
export PMAPORTS="/home/pmos/.local/var/pmbootstrap/cache_git/pmaports"
git -C "$PMAPORTS" checkout "$1"
pytest -vv test_upstream_compat.py
touch upstream-compat-"$1".check-passed
