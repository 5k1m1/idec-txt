#!/usr/bin/env python3

import api
import base64
import os
import sys
import urllib.request
from api import base
from api import fecho
from api import filter


def split(l, size=40):
    for i in range(0, len(l), size):
        yield l[i:i+size]


def download_index():
    msgids = []
    r = urllib.request.Request(
        "{0}u/e/{1}".format(api.node, "/".join(api.echoareas))
    )
    with urllib.request.urlopen(r) as f:
        raw = f.read().decode("utf-8").split()
        msgids = [msgid for msgid in raw if filter.is_msgid(msgid)]
    return msgids


def read_local_index():
    local = []
    for echoarea in api.echoareas:
        local += base.read_echoarea(echoarea)
    return local


def build_diff(local, remote):
    local = set(local)
    return [msgid for msgid in remote if msgid not in local]


def download_bundle(msgids):
    bundle = []
    print("fetch: {0}u/m/{1}".format(api.node, "/".join(msgids)))
    r = urllib.request.Request("{0}u/m/{1}".format(api.node, "/".join(msgids)))
    with urllib.request.urlopen(r) as f:
        bundle = f.read().decode("utf-8").split()
    return bundle


def debundle(bundle):
    for line in bundle:
        row = line.split(":")
        message = base64.urlsafe_b64decode(row[1]).decode("utf-8")
        echoarea = message.split("\n")[1]
        base.save_message(echoarea, row[0], message)
        open("newmail.txt", "a").write(
            api.render_message(row[0], message, True)
        )


def download_mail():
    index = build_diff(read_local_index(), download_index())
    open("newmail.txt", "w").write("")
    for s in split(index):
        debundle(download_bundle(s))


def read_local_fileindex():
    for fileechoarea in api.fileechoareas:
        for f in fecho.read_fechoarea(fileechoarea):
            yield f


def download_fecho_index():
    print("download file echoareas index")
    ids = []
    r = urllib.request.Request(
        "{0}f/e/{1}".format(api.node, "/".join(api.fileechoareas))
    )
    with urllib.request.urlopen(r) as f:
        raw = f.read().decode("utf-8").split("\n")
        fechoarea = ""
        for line in raw:
            if ":" not in line:
                fechoarea = line
            else:
                if len(line) > 0:
                    ids.append([fechoarea, line])
    return ids


def build_fileecho_diff(local, remote):
    return [i for i in remote if i not in local]


def download_file(fechoarea, fid):
    frow = fid.split(":")
    print("download: {0}f/f/{1}/{2} {3}".format(api.node, fechoarea,
                                                frow[0], frow[1]))
    r = urllib.request.Request(
        "{0}f/f/{1}/{2}".format(api.node, fechoarea, frow[0])
    )
    out = urllib.request.urlopen(r)
    fecho.save_file(fechoarea, frow, out)


def download_filemail():
    index = build_fileecho_diff(list(read_local_fileindex()),
                                download_fecho_index())
    if len(index) == 0:
        print("new files not found")
    for s in index:
        download_file(s[0], s[1])

        
base.check_base()
api.load_config()
download_mail()
api.mail_rebuild()
download_filemail()
