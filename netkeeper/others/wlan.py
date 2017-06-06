# coding=utf-8
import os

init = 'netsh wlan set hostednetwork mode=allow ssid=312 key=11223344'  # 设置热点帐号密码
start = 'netsh wlan start hostednetwork'  # 开启热点
stop = 'netsh wlan stop hostednetwork'  # 关闭热点
inited = False
opened = False

def open():
    if not inited:
        os.system(init)
    if not opened:
        os.system(start)


def close():
    if opened:
        os.system(stop)

open()