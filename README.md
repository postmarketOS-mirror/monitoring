# monitoring

Hourly monitoring of upstream compatibility with Alpine.

Running locally:
```sh
$ git clone https://gitlab.com/postmarketOS/pmbootstrap
$ git clone https://gitlab.com/postmarketOS/monitoring
$ cd monitoring
$ ln -s ../pmbootstrap/pmb .
$ export PMAPORTS=~/.local/var/pmbootstrap/cache_git/pmaports
$ pytest -xvv test_upstream_compat.py
```
