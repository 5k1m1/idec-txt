#!/usr/bin/env python3

import api, base64, os, sys, urllib.request
from api import base
from api import filter

def split(l, size=40):
    for i in range(0, len(l), size):
        yield l[i:i+size]

def download_index():
    msgids = []
    r = urllib.request.Request("%su/e/%s" % (api.node, "/".join(api.echoareas)))
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
    print("fetch: %su/m/%s" % (api.node, "/".join(msgids)))
    r = urllib.request.Request("%su/m/%s" % (api.node, "/".join(msgids)))
    with urllib.request.urlopen(r) as f:
        bundle = f.read().decode("utf-8").split()
    return bundle

def debundle(bundle):
    for line in bundle:
        row = line.split(":")
        message = base64.urlsafe_b64decode(row[1]).decode("utf-8")
        echoarea = message.split("\n")[1]
        base.save_message(echoarea, row[0], message)
        open("newmail.txt", "a").write(api.render_message(row[0], message, True))

def download_mail():
    index = build_diff(read_local_index(), download_index())
    open("newmail.txt", "w").write("")
    for s in split(index):
        debundle(download_bundle(s))

base.check_base()
api.load_config()
download_mail()
api.mail_rebuild()
