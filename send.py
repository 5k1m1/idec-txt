#!/usr/bin/env python3

import api
import base64
import os
import requests
import sys


node = ""
auth = ""


def get_local_echoareas():
    "Find directories of echoareas in mail/."
    for echoarea in os.scandir("mail/"):
        if echoarea.is_dir():
            yield(echoarea)


def find_new_messages():
    "Find all new message files."
    for echoarea in get_local_echoareas():
        for message in os.listdir("mail/{}".format(echoarea.name)):
            if message.endswith("new"):
                yield("mail/{0}/{1}".format(echoarea.name, message))


def read_message(filename):
    "Read message by filename."
    return open(filename, "r").read().split("\n")


def generate_message(filename):
    "Generate message for sending by filename."
    echoarea = filename.split("/")[1]
    message = read_message(filename)
    return "{0}\n{1}".format(echoarea, "\n".join(message))


def encode_message(message):
    "Base64 encode of message."
    return base64.b64encode(message.encode("utf-8"))


def send_mail():
    "Send all new message to uplink."
    global node, auth

    for filename in find_new_messages():
        message = generate_message(filename)
        encoded = encode_message(message)
        data = {"pauth": api.auth, "tmsg": encoded}
        try:
            requests.post(api.node + "u/point", data=data)
        except requests.exceptions.RequestException as exception:
            print("\n\n{}".format(exception))
            sys.exit(1)
        os.remove(filename)


api.load_config()
send_mail()
