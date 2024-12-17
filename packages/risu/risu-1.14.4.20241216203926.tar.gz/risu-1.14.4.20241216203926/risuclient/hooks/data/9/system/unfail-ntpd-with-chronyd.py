#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Description: Hook for removing failed ntpd status when chronyd is ok
# Author: Pablo Iranzo Gomez (Pablo.Iranzo@gmail.com)
# Copyright (C) 2018-2021, 2023 Pablo Iranzo Gómez <Pablo.Iranzo@gmail.com>
from __future__ import print_function

import os

try:
    import risuclient.shell as risu
except:
    import shell as risu

# Load i18n settings from risu
_ = risu._

extension = "__file__"
pluginsdir = os.path.join(risu.risudir, "plugins", extension)


def init():
    """
    Initializes module
    :return: List of triggers for extension
    """
    return []


def run(data, quiet=False, options=None):  # do not edit this line
    """
    Executes plugin
    :param quiet: be more silent on returned information
    :param data: data to process
    :return: returncode, out, err
    """

    # Use calculate ID instead of getid because of execution loop
    targetid = risu.calcid(string="/plugins/core/system/clock-1-ntpd.sh")
    sourceid = risu.calcid(string="/plugins/core/system/clock-1-chrony.sh")
    skipped = int(os.environ["RC_SKIPPED"])
    okay = int(os.environ["RC_OKAY"])

    mangle = False

    # Grab source data
    if sourceid in data and data[sourceid]["result"]["rc"] == okay:
        mangle = True

    if mangle and targetid in data:
        # We now fake result as SKIPPED and copy to datahook dict the new data
        data[targetid]["datahook"] = {}
        data[targetid]["datahook"]["prior"] = dict(data[targetid]["result"])
        newresults = dict(data[targetid]["result"])
        newresults["rc"] = skipped
        newresults["err"] = (
            "Marked as skipped by data hook %s"
            % os.path.basename(__file__).split(os.sep)[0]
        )
        data[targetid]["result"] = newresults
        risu.LOG.debug("Data mangled for plugin %s:" % data[targetid]["plugin"])

    return data


def help():  # do not edit this line
    """
    Returns help for plugin
    :return: help text
    """

    commandtext = _(
        "This hook proceses Risu outputs and unfails NTPD if chronyd is used"
    )
    return commandtext
