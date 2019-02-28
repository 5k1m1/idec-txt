import os

def check_base():
    if not os.path.exists("base"):
        os.makedirs("base")
    if not os.path.exists("base/echo"):
        os.makedirs("base/echo")
    if not os.path.exists("base/msg"):
        os.makedirs("base/msg")
    if not os.path.exists("idec.cfg"):
        open("idec.cfg", "w").write(open("idec.def.cfg").read())

def read_echoarea(echoarea):
    try:
        return open("base/echo/%s" % echoarea).read().split()
    except:
        return []

def read_message(msgid):
    try:
        return open("base/msg/%s" % msgid).read()
    except:
        return None

def save_message(echoarea, msgid, message):
    open("base/echo/%s" % echoarea, "a").write("%s\n" % msgid)
    open("base/msg/%s" % msgid, "w").write(message)
