# coding=utf-8
# !/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
1. 每隔一分钟检测一次服务状态
2. 如果发现服务状态已经停止，那么尝试启动服务
3. 自动记录日志
4. 任务栏图标显示
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import win32service
import logging
from logging.handlers import RotatingFileHandler
import os.path
import wx
import AppResource
import webbrowser
from AppXml import *

C_APP_NAME = "Service Moniter 1.0"
C_LOG_DIR = os.path.altsep.join([os.path.curdir, 'service.log'])
C_CONFIG_PATH = os.path.altsep.join([os.path.curdir, 'config.xml'])
C_LOG_SIZE = 1048576
C_LOG_FILES = 3
C_APP_SITE = "http://www.du52.com/?app=service_moniter&version=1.0.0"


class ServiceControl(object):
    def __init__(self):
        self.scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)

    # 检查服务是否停止
    def isStop(self, name):
        flag = False
        try:
            handle = win32service.OpenService(self.scm, name, win32service.SC_MANAGER_ALL_ACCESS)
            if handle:
                ret = win32service.QueryServiceStatus(handle)
                flag = ret[1] != win32service.SERVICE_RUNNING
                win32service.CloseServiceHandle(handle)
        except Exception, e:
            logging.error(e)
        return flag

    # 开启服务
    def start(self, name):
        try:
            handle = win32service.OpenService(self.scm, name, win32service.SC_MANAGER_ALL_ACCESS)
            if handle:
                win32service.StartService(handle, None)
                win32service.CloseServiceHandle(handle)
        except Exception, e:
            logging.error(e)

    # 退出
    def close(self):
        try:
            if self.scm:
                win32service.CloseServiceHandle(self.scm)
        except Exception, e:
            logging.error(e)


# 初始化日志
def InitLog():
    logging.getLogger().setLevel(logging.ERROR)
    RtHandler = RotatingFileHandler(filename=C_LOG_DIR, maxBytes=C_LOG_SIZE, backupCount=C_LOG_FILES)
    RtHandler.setLevel(logging.ERROR)
    RtHandler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s'))
    logging.getLogger().addHandler(RtHandler)
    logging.error('监控开始执行')


# 系统托盘图标
class TaskIcon(wx.TaskBarIcon):
    def __init__(self):
        wx.TaskBarIcon.__init__(self)
        self.SetIcon(AppResource.TaskIcon.getIcon(), C_APP_NAME)
        self.ID_NAME = wx.NewId()
        self.ID_EXIT = wx.NewId()
        self.ID_AUTHOR = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnExitEvent, id=self.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnHelpEvent, id=self.ID_AUTHOR)

    def OnHelpEvent(self, event):
        webbrowser.open_new(C_APP_SITE)

    def OnExitEvent(self, event):
        wx.Exit()

    def CreatePopupMenu(self, event=None):
        menu = wx.Menu()
        menu.Append(self.ID_NAME, C_APP_NAME)
        menu.AppendSeparator()
        menu.Append(self.ID_AUTHOR, "技术支持")
        menu.Append(self.ID_EXIT, "退出")
        return menu


# 隐藏窗口
class Frame(wx.Frame):
    def __init__(self, timelen, services):
        wx.Frame.__init__(self, parent=None, title=C_APP_NAME)
        self.timelen = timelen * 1000
        self.services = services
        self.Show(False)
        self.Bind(wx.EVT_TIMER, self.OnTimerEvent)
        self.Bind(wx.EVT_CLOSE, self.OnExitEvent)
        self.timer = wx.Timer(self)
        self.timer.Start(self.timelen)

    def OnTimerEvent(self, event):
        sc = ServiceControl()
        for name in self.services:
            print name
            if sc.isStop(name):
                logging.error('系统检测到服务[%s]停止' % (name,))
                sc.start(name)
        sc.close()

    def OnExitEvent(self, event):
        if self.timer:
            self.timer.Stop()
            self.timer = None


# 进程
class Application(wx.App):
    def OnInit(self):
        # 初始化配置
        xml = XmlNode()
        if not xml.LoadFile(C_CONFIG_PATH):
            logging.error('配置文件不存在')
            return False
        timelen = xml.FindNode('time').GetInt()
        if timelen <= 0:
            logging.error('监控间隔时间必须大于0秒')
            return False
        services = xml.FindNode('services').GetChildrenList(tag='item')
        if len(services) == 0:
            logging.error('监控服务列表不能为空')
            return False
        self.taskbar = TaskIcon()
        self.frame = Frame(timelen, services)
        return True

    def OnExit(self):
        logging.error('监控停止执行')
        self.frame.Close()
        self.taskbar.RemoveIcon()
        self.taskbar.Destroy()


if __name__ == '__main__':
    InitLog()
    app = Application()
    app.MainLoop()
