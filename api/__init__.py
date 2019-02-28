import os, shutil
from api import base
from datetime import datetime

node = ""
echoareas = []

def load_config():
    global node, echoareas
    node = ""
    echoareas = []
    config = open("idec.cfg").read().split("\n")
    for line in config:
        param = line.split()
        if len(param) > 0:
            if param[0] == "node":
                node = param[1]
            elif param[0] == "echo":
                echoareas.append(param[1])

def render_message(msgid, message, newmail = False):
    message = message.split("\n")
    rendered = "== [%s] %s ==============================\n" % (message[1], msgid) if newmail else "== %s ==============================\n" % msgid
    rendered += " From:    %s (%s) %s UTC\n" % (message[3], message[4], datetime.utcfromtimestamp(int(message[2])).strftime("%Y.%m.%d %a %H:%M"))
    rendered += " To:      %s\n" % message[5]
    rendered += " Subject: %s\n\n" % message[6]
    rendered += "\n".join(message[8:]) + "\n\n"
    return rendered

def mail_rebuild():
    print("Rebuild mail directory.")
    if os.path.exists("mail"):
        shutil.rmtree("mail")
    os.makedirs("mail")
    for echoarea in echoareas:
        os.makedirs("mail/%s" % echoarea)
        msgids = base.read_echoarea(echoarea)
        i = 0
        for msgid in msgids:
            open("mail/%s/%s.txt" % (echoarea, "%06d" % i), "w").write(render_message(msgid, base.read_message(msgid)))
            i += 1
