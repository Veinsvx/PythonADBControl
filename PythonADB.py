# -*- coding:utf-8 -*-
import uiautomator2 as u
from time import sleep
import os


def return_home():
    global d
    if d(text="米家").exists():
        print("回到米家首页了")
        d(text="米家").click()
        d(text="VR实验室").click()
        return 0
    else:
        d.press("back")
        print("没有回到米家首页，用递归查询")
        return_home()



def t_and_h():
    global d
    d(text="温湿度传感器").click()
    #等待元素出现，超过5秒钟不出现则返回flase
    if(d(text="Aqara温湿度传感器").wait(timeout=5.0)):
        tempdir1=d(text="湿度(%)").sibling(className="android.widget.TextView").info['text']
        tempdir2=d(text="温度(℃)").sibling(className="android.widget.TextView").info['text']  
        print("当前空气湿度："+tempdir1)
        print("当前空气温度："+tempdir2)


if __name__ == '__main__':
    #——————————————————————————————————————
    #第一次运行时，清除adb，连接模拟器，打开米家应用
    #os.system("adb kill-server")
    d=u.connect_adb_wifi("127.0.0.1:62001")
    d.app_start("com.xiaomi.smarthome")
    #——————————————————————————————————————
    sleep(5)#间隔几秒（等页面加载出来）
    return_home()
    sleep(5)
    t_and_h()
    