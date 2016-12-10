#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年12月1日
@author: Irony."[讽刺]
@site: alyl.vip, orzorz.vip, irony.coding.me , irony.iask.in , mzone.iask.in
@email: 892768447@qq.com
@file: PhotoEffects
@description: 
'''
import sys
import os

from time import strftime, localtime

from PyQt5.QtCore import Qt, QUrl, pyqtSlot
# from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtGui import QPalette
import data_rc



__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2016 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


#要实现透明的webview,需要先用一个QWidget作为父控件
class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_TranslucentBackground, True)#设置父控件Widget背景透明
        self.setWindowFlags(Qt.FramelessWindowHint)#去掉边框
        palette = self.palette()
        palette.setBrush(QPalette.Base, Qt.transparent)#父控件背景透明
        self.setPalette(palette)

        self.arrfiles = []#存放遍历的文件夹中的图片地址
#         QWebSettings.globalSettings().setAttribute(
#             QWebSettings.DeveloperExtrasEnabled, True)# web开发者工具
        
        self.webView = QWebView(self)#网页控件
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)#去掉右键菜单
        self.mainFrame = self.webView.page().mainFrame()
        self.mainFrame.javaScriptWindowObjectCleared.connect(
            self.setJavaScriptObject)#当网页加载时，自动执行setJavaScriptObject函数
        self.mainFrame.setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)#去掉滑动条
        self.mainFrame.setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        self.webView.load(QUrl('qrc:/index.html'))#加载网页

        self.showFullScreen()#全屏

    def setJavaScriptObject(self):#网页加载时自动执行，提供本地接口js对象MyWindow=self为本类实例
        self.mainFrame.addToJavaScriptWindowObject("MyWindow", self)
    
    def resizeEvent(self, event):#由于没有使用布局，这里当父窗口大小改变时自动改变webview的大小
        super(Window, self).resizeEvent(event)
        self.webView.resize(self.size())

    @pyqtSlot()
    def close(self):#提供给js调用
        super(Window, self).close()

    @pyqtSlot()
    def choose(self):#提供js调用选择文件夹功能
        _dir = QFileDialog.getExistingDirectory(self)
        if not _dir:
            return
        self.arrfiles.clear()
        for name in os.listdir(_dir):#遍历文件夹中的图片文件，没有做类型过滤
            path = os.path.join(_dir, name)
            stat = os.stat(path)
            size = stat.st_size / 1024
            time = strftime("%Y-%m-%d %H:%M:%S", localtime(stat.st_ctime))
            self.arrfiles.append({
                "name": "file:///" + path,
                "size": size,
                "time": time
            })
        self.webView.reload()  # 重新加载

    @pyqtSlot(result="QVariantList")
    def getArrfiles(self):
        return self.arrfiles#把之前遍历得到的图片文件数组返回给js

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
