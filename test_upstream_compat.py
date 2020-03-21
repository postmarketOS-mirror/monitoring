#!/usr/bin/env python3
# Copyright 2020 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import glob
import os
import pytest

import pmb.helpers.logging
import pmb.parse.apkindex
import pmb.parse


@pytest.fixture
def args(request):
    # Initialize args
    sys.argv = ["pmbootstrap",
                "--aports", os.environ["PMAPORTS"],
                "chroot"]
    args = pmb.parse.arguments()

    # Initialize logging
    pmb.helpers.logging.init(args)
    request.addfinalizer(args.logfd.close)
    return args


def test_qt_versions(args):
    """
    Verify, that all postmarketOS qt5- package versions match with Alpine's
    qt5-qtbase version.
    """
    # Upstream version
    index = pmb.helpers.repo.alpine_apkindex_path(args, "community", "x86_64")
    index_data = pmb.parse.apkindex.package(args, "qt5-qtbase",
                                            indexes=[index])
    pkgver_upstream = index_data["version"].split("-r")[0]

    # Iterate over our packages
    failed = []
    for path in glob.glob(args.aports + "/*/qt5-*/APKBUILD"):
        # Read the pkgver
        apkbuild = pmb.parse.apkbuild(args, path)
        pkgname = apkbuild["pkgname"]
        pkgver = apkbuild["pkgver"]

        # When we temporarily override packages from Alpine, we set the pkgver
        # to 9999 and _pkgver contains the real version (see #994).
        if pkgver == "9999":
            pkgver = apkbuild["_pkgver"]

        # We had to add a few qt5 git packages for unity8 (!27), obviously we
        # can't compare the version there.
        if "_git" in pkgver:
            continue

        # Compare
        if pkgver == pkgver_upstream:
            continue
        failed.append(pkgname + ": " + pkgver + " != " +
                      pkgver_upstream)

    assert [] == failed


def test_aportgen_versions(args):
    """
    Verify that the packages generated by 'pmbootstrap aportgen' have
    the same version (pkgver *and* pkgrel!) as the upstream packages
    they are based on.
    """
    # Get Alpine's "main" repository APKINDEX path
    index = pmb.helpers.repo.alpine_apkindex_path(args, "main", "x86_64")

    # Alpine packages and patterns for our derivatives
    map = {"binutils": "binutils-*",
           "busybox": "busybox-static-*",
           "gcc": "gcc-*",
           "grub": "grub-efi-*",
           "musl": "musl-*"}

    # Iterate over Alpine packages
    failed = []
    generated = "# Automatically generated aport, do not edit!"
    for pkgname, pattern in map.items():
        # Upstream version
        index_data = pmb.parse.apkindex.package(args, pkgname,
                                                indexes=[index])
        version_upstream = index_data["version"]

        # Iterate over our packages
        for path in glob.glob(args.aports + "/*/" + pattern + "/APKBUILD"):
            # Skip non-aportgen APKBUILDs
            with open(path) as handle:
                if generated not in handle.read():
                    continue

            # Compare the version
            print("Checking " + path)
            apkbuild = pmb.parse.apkbuild(args, path)
            version = apkbuild["pkgver"] + "-r" + apkbuild["pkgrel"]
            if version != version_upstream:
                failed.append(apkbuild["pkgname"] + ": " + version +
                              " != " + version_upstream +
                              " (from " + pkgname + ")")
                continue

    assert [] == failed


def test_soname_bump(args):
    """ Use pmb.helpers.pkgrel_bump to check if the pmaports need a pkgrel bump
        caused by a soname bump in Alpine. Example: a new openssl version was
        released, which increased the soname version, and now all packages that
        link against it, need to be rebuilt. """
    if pmb.helpers.pkgrel_bump.auto(args, True):
        raise RuntimeError("One or more packages need to be rebuilt, because"
                           " a library they link against had an incompatible"
                           " upgrade (soname bump). Run 'pmbootstrap"
                           " pkgrel_bump --auto' to automatically increase the"
                           " pkgrel in order to trigger a rebuild.")