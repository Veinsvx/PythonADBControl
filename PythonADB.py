# -*- coding:utf-8 -*-
import uiautomator2 as u
from time import sleep
import os


#调用后返回米家首页
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



#获取温湿度传感器的数据
def t_and_h():
    global d
    d(text="温湿度传感器").click()
    #等待元素出现，超过5秒钟不出现则返回flase
    if(d(text="Aqara温湿度传感器").wait(timeout=5.0)):
        tempdir1=d(text="湿度(%)").sibling(className="android.widget.TextView").info['text']
        tempdir2=d(text="温度(℃)").sibling(className="android.widget.TextView").info['text']  
        print("当前空气湿度："+tempdir1)
        print("当前空气温度："+tempdir2)


#灯全开
def all_light_on():
    global d
    d(text="场景").click()
    d(text="自定义").click()
    d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/c6v"]/android.widget.RelativeLayout[1]/android.view.View[1]/android.widget.RelativeLayout[2]/android.widget.FrameLayout[1]/android.widget.TextView[1]').click()
    return_home()

#灯全关
def all_light_off():
    global d
    d(text="场景").click()
    d(text="自定义").click()
    d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/c6v"]/android.widget.RelativeLayout[2]/android.view.View[1]/android.widget.RelativeLayout[2]/android.widget.FrameLayout[1]/android.widget.TextView[1]').click()
    return_home()

#窗帘全开
def all_curtain_on():
    global d
    d(text="场景").click()
    d(text="自定义").click()
    d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/c6v"]/android.widget.RelativeLayout[3]/android.view.View[1]/android.widget.RelativeLayout[2]/android.widget.FrameLayout[1]/android.widget.TextView[1]').click()
    return_home()

#窗帘全关
def all_curtain_off():
    global d
    d(text="场景").click()
    d(text="自定义").click()
    d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/c6v"]/android.widget.RelativeLayout[4]/android.view.View[1]/android.widget.RelativeLayout[2]/android.widget.FrameLayout[1]/android.widget.TextView[1]').click()
    return_home()

#关闭或打开指定灯
def close_or_open_specify_light(index):
    if index!= None:
        if index != 2:
            d(text="灯%d"%(index)).click()
            d(text="左键").click()
            d(text="右键").click()
        else:
            d(text="灯%d"%(index)).click()
            #d(text="某按键").click()
    else:
        print("输入有误")

#打开指定窗帘 //待测试-目测点击文本无法触发功能
def open_specify_curtain(index):
    if index!= None:
        d(text="窗帘%d"%(index)).click()
        d(text="打开").click()
    else:
        print("输入有误")

#关闭指定窗帘 //待测试-目测点击文本无法触发功能
def close_specify_curtain(index):
    if index!= None:
        d(text="窗帘%d"%(index)).click()
        d(text="关闭").click()
    else:
        print("输入有误")

#被调用时，设置家居场景为默认状态
def once_nomal_state():
    global d
    d(text="场景").click()
    d(text="自定义").click()
    d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/c6v"]/android.widget.RelativeLayout[5]/android.view.View[1]/android.widget.RelativeLayout[2]/android.widget.FrameLayout[1]/android.widget.TextView[1]').click()
    return_home()


if __name__ == '__main__':
    #——————————————————————————————————————
    #第一次运行时，清除adb，连接模拟器，打开米家应用
    #os.system("adb kill-server")
    d=u.connect_adb_wifi("127.0.0.1:62001")
    d.app_start("com.xiaomi.smarthome")
    #——————————————————————————————————————
    #鉴于通过ui包无法合理获取到电灯、插座和窗帘的运行状态，目前快速完成方案为python被unity调用运行时，把所有的灯和窗帘设置为关闭、插座为开启状态。
    return_home()
    once_nomal_state()
    #——————————————————————————————————————
    #测试功能
    sleep(5)#间隔几秒（等页面加载出来）