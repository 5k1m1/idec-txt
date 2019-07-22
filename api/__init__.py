import os
import shutil
import sys
from api import base
from datetime import datetime

node = ""
auth = ""
echoareas = []
fileechoareas = []


def load_config():
    global node, auth, echoareas, fileechoareas
    node = ""
    echoareas = []
    try:
        config = open("idec.cfg").read().split("\n")
    except FileNotFoundError as exception:
        print(exception)
        sys.exit(1)

    for line in config:
        param = line.split()
        if len(param) > 0:
            if param[0] == "node":
                node = param[1]
            elif param[0] == "auth":
                auth = param[1]
            elif param[0] == "echo":
                echoareas.append(param[1])
            elif param[0] == "fecho":
                fileechoareas.append(param[1])


def render_message(msgid, message, newmail=False):
    message = message.split("\n")
    time = datetime.utcfromtimestamp(int(message[2]))
    time = time.strftime("%Y.%m.%d %a %H:%M")
    delim1 = "== [{0}] {1} {2}\n".format(message[1], msgid, "=" * 30)
    delim2 = "== {0} {1}\n".format(msgid, "=" * 30)
    rendered = delim1 if newmail else delim2
    rendered += " From:    {0} ({1}) {2} UTC\n".format(message[3],
                                                       message[4], time)
    rendered += " To:      {}\n".format(message[5])
    rendered += " Subject: {}\n\n".format(message[6])
    rendered += "\n".join(message[8:]) + "\n\n\n"
    return rendered


def mail_rebuild():
    print("Rebuild mail directory.")
    if os.path.exists("mail"):
        shutil.rmtree("mail")
    os.makedirs("mail")
    for echoarea in echoareas:
        os.makedirs("mail/{}".format(echoarea))
        msgids = base.read_echoarea(echoarea)
        i = 0
        for msgid in msgids:
            n = "{:06d}".format(i)
            open("mail/{0}/{1}.txt".format(echoarea, n), "w").write(
                render_message(msgid, base.read_message(msgid))
            )
            i += 1
