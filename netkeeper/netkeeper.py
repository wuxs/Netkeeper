# coding=utf-8
import os
import threading
import time
import win32ras

import settings
from log import logger


class Netkeeper(object):
    def __init__(self):
        self._auto = True
        self.state = True

    # 断开网络连接
    def disconnect(self):
        flag = self.get_conn()
        if len(flag) == 1:
            handle = flag[0][0]
            dialname = str(flag[0][1])
            try:
                win32ras.HangUp(handle)
                self.saveData(False, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                logger.info("连接" + dialname + "已断开！")
                return True
            except Exception as e:
                logger.info(dialname + "断开连接失败！" + str(e.message))
                # disconnect()
        else:
            logger.info("错误的进程号或当前无连接！")

    # 获取已拨号的连接
    def get_conn(self):
        connections = win32ras.EnumConnections()
        return connections

    # 拨号
    def connect(self, account, password, dialname='Netkeeper'):
        dial_params = (dialname, '', '', account, password, '')
        logger.info(str(dial_params))
        return win32ras.Dial(None, None, dial_params, None)
        # logger.info(str(_handler) + '  ' + str(result))

    # 获取加密后的帐号
    def getRealAccount(self, account):
        # 使用pyjnius，调用java代码的加密算法 ，获取真正的登录帐号
        os.environ['CLASSPATH'] = os.path.join(os.path.dirname(__file__), 'bin')
        from jnius import autoclass
        RealAccount = autoclass('test.RealAccount')
        real = RealAccount(account)
        realname = real.Realusername()
        return realname

    def check_loop(self):
        while settings.RUNNING:
            conns = self.get_conn()
            if not conns:
                pass

    # 掉线自动重连
    def autoDail(self, account, password, callback):
        retrytimes = 0  # 重试次数
        max_retry = 3  # 最大重试次数
        dial_name = 'Netkeeper'
        while settings.RUNNING:
            conns = self.get_conn()
            if not conns:
                real_account = self.getRealAccount(account)
                handle, result = self.connect(real_account, password, dial_name)
                if result == 0:
                    curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    self.saveData(True, curtime)
                    threading.Thread(target=callback, args=(time.time(), 13213132313))
                    logger.info("E信登录成功!    " + repr(account))
                elif result == 691:
                    self.disconnect()
                    if retrytimes == max_retry:
                        logger.info("重试次数过多！取消拨号！")
                        return
                    reason = win32ras.GetErrorString(result).decode('GBK').encode('utf-8')
                    logger.info("登录失败!  " + reason + "(Code:" + result + ")")
                    logger.info("3秒后重试")
                    time.sleep(3)
                    retrytimes += 1
                elif result == 623:
                    dial_name = dial_name[4:] if 'Simp' in dial_name else 'SimpNetkeeper'
            else:
                time.sleep(30)

    # 设置掉线自动登录
    def setAuto(self, flag):
        self._auto = flag

    # 将上网时长保存到文本中
    def saveData(self, state, curtime):
        with open('E:/NKService/records.txt', 'a+') as f:
            if state:
                f.write(curtime + "    登录\n")
            else:
                f.write(curtime + "    退出\n")


#
# # 断开网络连接
# def disconnect():
#     flag = get_conn()
#     if len(flag) == 1:
#         handle = flag[0][0]
#         dialname = str(flag[0][1])
#         try:
#             win32ras.HangUp(handle)
#             saveData(False, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
#             logger.info("连接" + dialname + "已断开！")
#             return True
#         except Exception as e:
#             logger.info(dialname + "断开连接失败！" + str(e.message))
#             # disconnect()
#     else:
#         logger.info("错误的进程号或当前无连接！")
#
#
# # 获取已拨号的连接
# def get_conn():
#     connections = win32ras.EnumConnections()
#     return connections
#
#
# # 拨号
# def connect(account, password, dialname='Netkeeper'):
#     dial_params = (dialname, '', '', account, password, '')
#     logger.info(str(dial_params))
#     return win32ras.Dial(None, None, dial_params, None)
#     # logger.info(str(_handler) + '  ' + str(result))
#
#
# # 获取加密后的帐号
# def getRealAccount(account):
#     # 使用pyjnius，调用java代码的加密算法 ，获取真正的登录帐号
#     os.environ['CLASSPATH'] = os.path.join(os.path.dirname(__file__), 'bin')
#     from jnius import autoclass
#     RealAccount = autoclass('test.RealAccount')
#     real = RealAccount(account)
#     realname = real.Realusername()
#     return realname
#
#
# # 掉线自动重连
# def autoDail(account, password, callback):
#     retrytimes = 0  # 重试次数
#     max_retry = 3  # 最大重试次数
#     dial_name = 'Netkeeper'
#     while settings.RUNNING:
#         conns = get_conn()
#         if not conns and _auto:
#             realaccount = getRealAccount(account)
#             handle, result = connect(realaccount, password, dial_name)
#             if result == 0:
#                 # session.add(NKTime(mdate='', starttime='', endtime='', totaltime=''))
#                 saveData(True, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
#                 threading.Thread(target=callback)
#                 logger.info("E信登录成功!    " + repr(account))
#             elif result == 691:
#                 disconnect()
#                 if retrytimes == max_retry:
#                     logger.info("重试次数过多！取消拨号！")
#                     return
#                 reason = win32ras.GetErrorString(result).decode('GBK').encode('utf-8')
#                 logger.info("登录失败!  " + reason + "(Code:" + result + ")")
#                 logger.info("3秒后重试")
#                 time.sleep(3)
#                 retrytimes += 1
#             elif result == 623:
#                 dial_name = dial_name[4:] if 'Simp' in dial_name else 'SimpNetkeeper'
#         else:
#             time.sleep(60)
#
#
# # 设置掉线自动登录
# def setAuto(flag):
#     global _auto
#     _auto = flag
#
#
# # 将上网时长保存到文本中
# def saveData(state, curtime):
#     with open('E:/NKService/records.txt', 'a+') as f:
#         if state:
#             f.write(curtime + "    登录\n")
#         else:
#             f.write(curtime + "    退出\n")
#

if __name__ == '__main__':
    # autoDail('xxxxxx@hkd', 'xxxxx')
    # disconnect()
    print ''
