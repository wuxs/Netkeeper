# coding=utf-8
import Tkinter
import os
import time
import win32api
import win32gui

import win32con
import winerror

import settings

'''
# -*- coding: cp936 -*-
# <Button-1>：鼠标左击事件
# <Button-2>：鼠标中击事件
# <Button-3>：鼠标右击事件
# <Double-Button-1>：双击事件
# <Triple-Button-1>：三击事件
# <Bx-Motion>：鼠标移动事件,x=[1,2,3]分别表示左、中、右鼠标操作。
# <ButtonRelease-x>鼠标释放事件,x=[1,2,3],分别表示鼠标的左、中、右键操作
# <Enter>：鼠标释放事件
'''


def gbk(string):
    return string.decode('utf-8').encode('gbk')


class MainWindow(object):
    # _size = {'w': 120, 'h': 70, 'x': 1500, 'y': 800}
    _size = '120x70+1500+800'
    _last_position = ''
    _moveable = True
    _clickable = True

    def __init__(self, size=_size):
        self._size = size
        self.root = Tkinter.Tk()
        self.root.overrideredirect(True)
        self.root.configure(bg='black')
        self.root.attributes("-transparentcolor", "black")
        self.root.attributes('-topmost', 1)
        self.root.attributes("-alpha", 1)  # 窗口透明度
        self.root.geometry(self._size)
        self.timelabel = Tkinter.Label(self.root, text="01:12:56", font=('consolas', 18), fg="white", bg='black',
                                       width=100)
        self.totallabel = Tkinter.Label(self.root, text="00:12:56", font=('consolas', 18), fg="white", bg='black',
                                        width=100)
        self.timelabel.pack()
        self.totallabel.pack()

        self.root.bind('<B1-Motion>', self.move)  # 移动
        self.root.bind('<Button-1>', self.left_click)  # 点击左键
        self.root.bind('<Triple-Button-1>', self.triple_click)  # 左键三击
        self.root.destroy()

    def mainloop(self):
        self.root.mainloop()

    def destory(self):
        self.root.destroy()

    def autoupdate(self, start, total):
        while settings.RUNNING:
            nowtime = time.time()
            runtime = nowtime - start
            timestr = time.strftime('%H:%M:%S', time.gmtime(runtime))
            self.update(self.timelabel, timestr)
            time.sleep(1)

    def update(self, target, value):
        target['text'] = value

    def clickable(self, value):
        self._clickable = value

    def moveable(self, value):
        self._moveable = value

    def move(self, event):
        if not self._moveable:
            return
        cur_x = (event.x - self.last_x) + self.root.winfo_x()
        cur_y = (event.y - self.last_y) + self.root.winfo_y()
        self._size = self._size[:self._size.find('+') + 1] + str(cur_x) + "+" + str(cur_y)
        # print cur_x, cur_y,new_size
        self.root.geometry(self._size)

    def left_click(self, event):
        self.last_x, self.last_y = event.x, event.y
        # print("event.x, event.y = ", event.x, event.y)

    def triple_click(self, event):
        self.hide()
        time.sleep(3)
        self.show()

    def fade_in(self):
        alpha = self.root.attributes("-alpha")
        alpha = min(alpha + .01, 1.0)
        self.root.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.root.after(10, self.fade_in)
            # time.sleep(0.01)
            # self.fade_in()

    def fade_out(self):
        alpha = self.root.attributes("-alpha")
        alpha = max(alpha - .01, 0)
        self.root.attributes("-alpha", alpha)
        if alpha > 0:
            self.root.after(10, self.fade_out)
            # time.sleep(0.01)
            # self.fade_out()

    def hide(self):
        # self.fade_out()
        self._last_position = self._size
        self.root.withdraw()

    def show(self):
        self.root.update()
        self.root.deiconify()
        self.root.geometry(self._last_position)
        # self.fade_in()


class TrayIcon(object):
    def __init__(self, netkeeper):
        msg_TaskbarRestart = win32gui.RegisterWindowMessage("NKService")
        message_map = {
            msg_TaskbarRestart: self.OnRestart,
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_COMMAND: self.OnCommand,
            win32con.WM_USER + 20: self.OnTaskbarNotify,
        }
        # 注册窗口类
        wndclass = win32gui.WNDCLASS()
        hinst = wndclass.hInstance = win32api.GetModuleHandle(None)
        wndclass.lpszClassName = "NetkeeperTrayIcon"
        wndclass.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wndclass.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        wndclass.hbrBackground = win32con.COLOR_WINDOW
        wndclass.lpfnWndProc = message_map
        try:
            classAtom = win32gui.RegisterClass(wndclass)
        except win32gui.error, err_info:
            if err_info.winerror != winerror.ERROR_CLASS_ALREADY_EXISTS:
                raise
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(wndclass.lpszClassName, 'NetKeeper Service', style, 0, 0,
                                          win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        self.netkeeper = netkeeper
        self._createIcon()

    def _createIcon(self):
        hinst = win32api.GetModuleHandle(None)
        iconPathName = ""
        if os.path.isfile(iconPathName):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        else:
            print '未找到icon文件，使用默认'
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "NetKeeper Service")
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except win32gui.error:
            print "Failed to add the taskbar icon - is explorer running?"

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._createIcon()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONUP:
            print "You clicked me."
        elif lparam == win32con.WM_LBUTTONDBLCLK:
            print "You double-clicked me - goodbye"
            win32gui.DestroyWindow(self.hwnd)
        elif lparam == win32con.WM_RBUTTONUP:
            print "You right clicked me."
            menu = win32gui.CreatePopupMenu()
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1023, gbk("切换帐号"))
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, gbk("切换帐号"))
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, gbk("断开连接"))
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1026, gbk("退出服务"))
            pos = win32gui.GetCursorPos()
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)
        if id == 1023:
            print '1023'
        elif id == 1024:
            print "切换帐号"
        elif id == 1025:
            self.netkeeper.disconnect()
            print "断开连接"
        elif id == 1026:
            print "退出服务"
            settings.RUNNING = False
            win32gui.DestroyWindow(self.hwnd)
        else:
            print "Unknown command -", id


if __name__ == '__main__':
    # t = TrayIcon()
    # win32gui.PumpMessages()
    w = MainWindow()
    import threading
    thread1 = threading.Thread(target=w.autoupdate)
    thread1.setDaemon(True)
    thread1.start()
    w.mainloop()
