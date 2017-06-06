# coding=utf-8
import threading
import win32event
import win32service

import win32serviceutil

import init
from netkeeper import Netkeeper
from log import logger
from NKUI import MainWindow,TrayIcon


class NKService(win32serviceutil.ServiceFramework):
    _svc_name_ = "NKService"
    _svc_display_name_ = "NKService"
    _svc_description_ = "NetKeeper ..."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = logger
        self.run = True

    def SvcDoRun(self):
        self.logger.info("Service start ")
        init.init()
        if init.settings.RUNNING:
            self.netkeeper = Netkeeper()
            self.mainwindow = MainWindow()
            thread1 = threading.Thread(target=self.netkeeper.autoDail,
                                       args=('17702737125@hkd', '09152287', self.mainwindow.autoupdate))
            thread1.setDaemon(True)
            thread1.start()
            thread2 = threading.Thread(target=self.mainwindow.mainloop())
            thread2.setDaemon(True)
            thread2.start()
            self.tray=TrayIcon(self.netkeeper)
            # account, password = confparser.getAcc()
            # netkeeper.autoDail('17702737125@hkd', '09152287',mainwindow.update)

    def SvcStop(self):
        self.netkeeper.disconnect()
        self.logger.info("service is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False

    '''
    1.安装服务

    python NKService.py install

    2.让服务自动启动

    python NKService.py --startup auto install

    3.启动服务

    python NKService.py start

    4.重启服务

    python NKService.py restart

    5.停止服务

    python NKService.py stop

    6.删除/卸载服务

    python PythonService.py remove
    '''


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(NKService)
