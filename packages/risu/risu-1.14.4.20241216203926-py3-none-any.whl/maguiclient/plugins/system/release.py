#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Description: Plugin for checking RH Release across hosts
# Copyright (C) 2018-2021, 2023 Pablo Iranzo Gómez <Pablo.Iranzo@gmail.com>
from __future__ import print_function

try:
    import risuclient.shell as risu
except:
    import shell as risu

# Load i18n settings from risu
_ = risu._

extension = "release"


def init():
    """
    Initializes module
    :return: List of triggers for Plugin
    """
    ids = risu.getids(include=["/metadata/system/release.sh"])
    return ids


def run(data, quiet=False):  # do not edit this line
    """
    Executes plugin
    :param quiet: reduce amount of data returned
    :param data: data to process
    :return: returncode, out, err
    """

    returncode = risu.RC_OKAY

    message = ""
    for ourdata in data:
        # 'err' in this case should be always equal to the md5sum of the file so that we can report the problem
        err = [
            data[ourdata]["sosreport"][sosreport]["err"]
            for sosreport in data[ourdata]["sosreport"]
        ]

        if len(sorted(set(err))) != 1:
            message = _(
                "Hosts contains different releases of operating system and can cause issues."
            )
            returncode = risu.RC_FAILED

    out = ""
    err = message
    return returncode, out, err


def help():  # do not edit this line
    """
    Returns help for plugin
    :return: help text
    """

    commandtext = _("This plugin checks uniform releasing of OS across sosreports")
    return commandtext
