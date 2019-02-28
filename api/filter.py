import re

def is_msgid(msgid):
    return re.match("[0-9a-zA-Z]{20}", msgid)

def is_echoarea(echoarea):
    return re.match("[0-9a-z_\-\.]{1,60}\.[0-9a-z_\-\.]{1,60}", echoarea)
