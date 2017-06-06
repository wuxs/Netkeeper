# coding=utf-8

# 初始化程序数据
import settings
import os


def init():
    # 初始化文件目录
    if not os.path.exists(settings.OUTPUT_PATH):
        try:
            os.makedirs(settings.OUTPUT_PATH)
        except:
            print "创建目录失败！"
            settings.RUNNING = False
            return
    settings.RUNNING = True
