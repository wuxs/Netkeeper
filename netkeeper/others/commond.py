# coding=utf-8

# 初始化热点
initwlan = 'netsh wlan set hostednetwork mode=allow ssid=312 key=11223344'
start = 'netsh wlan start hostednetwork'  # 开启热点
stop = 'netsh wlan stop hostednetwork'  # 关闭热点

shutdown = 'shutdown -s -t 1'  # 1s后关机
