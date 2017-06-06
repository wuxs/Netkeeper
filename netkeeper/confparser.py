# coding=utf-8
import ConfigParser

from netkeeper.settings import CONFIG_FILE

items = None


def _init():
    cp = ConfigParser.SafeConfigParser()
    cp.read(CONFIG_FILE)
    global items
    items = cp.items('default')


def getAcc():
    if not items:
        _init()
    account = items[0]
    password = items[1]
    return account[1], password[1]


def getPath():
    return items['output']
