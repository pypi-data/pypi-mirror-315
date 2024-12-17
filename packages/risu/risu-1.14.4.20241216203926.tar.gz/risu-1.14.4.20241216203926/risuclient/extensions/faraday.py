#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Description: Extension for processing file affinities/antiaffinities to be reported in a
#              similar way to metadata and later processed by corresponding plugin in Magui
#
# Author: Pablo Iranzo Gomez (Pablo.Iranzo@gmail.com)
# Copyright (C) 2018-2021, 2023 Pablo Iranzo Gómez <Pablo.Iranzo@gmail.com>
from __future__ import print_function

import hashlib
import os

try:
    import risuclient.shell as risu
except:
    import shell as risu

# Load i18n settings from risu
_ = risu._

extension = "faraday"
pluginsdir = os.path.join(risu.risudir, "plugins", extension)


def init():
    """
    Initializes module
    :return: List of triggers for extension
    """
    triggers = ["faraday"]
    return triggers


def listplugins(options=None):
    """
    List available plugins
    :param options: argparse options provided
    :return: plugin object generator
    """

    prio = 0
    if options:
        try:
            prio = options.prio
        except:
            pass

    if options and options.extraplugintree:
        folders = [pluginsdir, os.path.join(options.extraplugintree, extension)]
    else:
        folders = [pluginsdir]

    plugins = risu.findplugins(
        folders=folders,
        executables=False,
        fileextension=".txt",
        extension=extension,
        prio=prio,
        options=options,
    )
    # check for multiple files specified as per the 'path' by using "," as separator

    newplugins = []
    for plugin in plugins:
        if "," not in plugin["path"]:
            newplugins.append(plugin)
        else:
            # Path contains ',' so we fake extra plugins for each path
            for path in plugin["path"].split(","):
                # Clone plugin dictionary:
                newplugin = dict(plugin)
                newplugin["name"] = "Check %s" % path.replace("${RISU_ROOT}", "")
                newplugin["path"] = path
                newplugin["description"] = "%s: %s" % (
                    plugin["description"],
                    path.replace("${RISU_ROOT}", ""),
                )
                newplugin["id"] = "%s-%s" % (plugin["id"], risu.calcid(string=path))
                newplugins.append(newplugin)

    yield newplugins


def get_metadata(plugin):
    """
    Gets metadata for plugin
    :param plugin: plugin object
    :return: metadata dict for that plugin
    """

    return risu.generic_get_metadata(plugin)


def run(plugin):  # do not edit this line
    """
    Executes plugin
    :return: returncode, out, err
    """
    filename = plugin["path"]

    skipped = 0
    if os.environ["RISU_LIVE"] == 0 and risu.regexpfile(
        filename=filename, regexp="RISU_ROOT"
    ):
        # We're running in snapshoot and faraday file has RISU_ROOT
        skipped = 0
    else:
        if os.environ["RISU_LIVE"] == 1:
            if risu.regexpfile(
                filename=plugin["plugin"], regexp="RISU_HYBRID"
            ) or not risu.regexpfile(filename=filename, regexp="RISU_ROOT"):
                # We're running in Live mode and either plugin supports HYBRID or has no RISU_ROOT
                skipped = 0
            else:
                # We do not satisfy conditions, exit early
                skipped = 1

    if skipped == 1:
        return (
            risu.RC_SKIPPED,
            "",
            _("Plugin does not satisfy conditions for running"),
        )

    if "${RISU_ROOT}" in filename:
        filename = filename.replace("${RISU_ROOT}", os.environ["RISU_ROOT"])

    if os.access(filename, os.R_OK):
        # We can read the file, so let's calculate md5sum
        out = ""
        err = hashlib.sha512(open(filename, "rb").read()).hexdigest()
        returncode = risu.RC_OKAY
    else:
        returncode = risu.RC_SKIPPED
        out = ""
        err = "File %s is not accessible in read mode" % filename

    return returncode, out, err


def help():  # do not edit this line
    """
    Returns help for plugin
    :return: help text
    """

    commandtext = _(
        "This extension creates fake plugins based on affinity/antiaffinity file list for later processing"
    )
    return commandtext
