# -*- coding:utf-8 -*-
import uiautomator2 as u
from time import sleep
import os
import socket
import threading



#暂时弃用双向通信方式，从while中直接开启message_receiver线程，若日后启用，改为on_new_connection即可
#当新的客户端连入时会调用这个方法
#def on_new_connection(client_executor, addr):
#    print('从%s:%s进行一个连接...' % addr)
#    #开启一个线程等待接收数据
#    recy_thread=threading.Thread(target=message_receiver, args=(client_executor,addr))
#    recy_thread.start()
    
    #data=""
    #while True:
    #    result=instance.read()
    #    if result.is_valid():
    #        print("Temperature: %-3.1f C" % result.temperature)
    #        print("Humidity: %-3.1f %%" % result.humidity)
    #        data="h%.1f,t%.1f"%(result.humidity,result.temperature)
    #        client_executor.send(data.encode('utf-8'))
    #    else:
    #        print("Error: %d" % result.error_code)
    #        GPIO.cleanup()
    #        time.sleep(10)
    #        continue
    #    time.sleep(30)
    #clent_executor.close()
    #print("接受信息的目标计算机%s:%s断开链接"%addr)

#接收客户端发送过来的数据
def message_receiver(client_executor,addr):
    while True:
        msg = client_executor.recv(1024).decode('utf-8')
        print(msg)
        if msg == 'exit':
            print('%s:%s发送关闭连接请求' % addr)
            break
        elif msg=="tah" :#获取温湿度信息
          client_executor.send(t_and_h().encode('utf-8'))        
        elif msg=="aln":#打开所有灯
            all_light_on()
        elif msg=="alf" :#关闭所有灯
            all_light_off()
        elif msg=="acn" :#打开所有窗帘
            all_curtain_on()
        elif msg=="acf":#关闭所有窗帘
            all_curtain_off()
        elif "sl" in msg :#打开或关闭指定灯
            print(msg[2:])
            close_or_open_specify_light(msg[2:])
        elif "osc" in msg :#打开指定窗帘
            print(msg[3:])
            open_specify_curtain(msg[3:])
        elif "csc" : #关闭指定窗帘
            close_specify_curtain(msg[3:])
        elif msg=="ons":#恢复家居场景为默认状态
            once_nomal_state()
        else:
            print("接收%s:%s数据有问题，请检查unity客户端发送数据或网络连接"%addr)
    client_executor.close()
    print("发送信息的目标计算机%s:%s断开链接"%addr)
       


#调用后返回米家首页
def return_home():
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
    d(text="温湿度传感器").click()
    #等待元素出现，超过5秒钟不出现则返回flase
    if(d(text="Aqara温湿度传感器").wait(timeout=5.0)):
        tempdir1=d(text="湿度(%)").sibling(className="android.widget.TextView").info['text']
        tempdir2=d(text="温度(℃)").sibling(className="android.widget.TextView").info['text']  
        print("当前空气湿度："+tempdir1)
        print("当前空气温度："+tempdir2)
        return "h%s,t%s"%(tempdir1,tempdir2)

#灯全开
def all_light_on():
    d(text="场景").click()
    d(text="自定义").click()
    #xpath点击有问题，暂时弃用
    #d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/ca7"]/android.widget.RelativeLayout[1]/android.view.View[1]/android.widget.RelativeLayout[2]/android.widget.FrameLayout[1]/android.widget.TextView[1]').click()
    d.click(0.886, 0.333)
    return_home()

#灯全关
def all_light_off():
    d(text="场景").click()
    d(text="自定义").click()
    #xpath点击有问题，暂时弃用
    #d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/ca7"]/android.widget.RelativeLayout[2]/android.view.View[1]/android.widget.RelativeLayout[2]/android.widget.FrameLayout[1]/android.widget.TextView[1]').click()
    d.click(0.888, 0.469)
    return_home()

#窗帘全开
def all_curtain_on():
    d(text="场景").click()
    d(text="自定义").click()
    #xpath点击有问题，暂时弃用
    #d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/ca7"]/android.widget.RelativeLayout[3]/android.view.View[1]/android.widget.RelativeLayout[2]/android.widget.FrameLayout[1]/android.widget.TextView[1]').click()
    d.click(0.906, 0.6)
    return_home()

#窗帘全关
def all_curtain_off():
    d(text="场景").click()
    d(text="自定义").click()
    #xpath点击有问题，暂时弃用
    #d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/ca7"]/android.widget.RelativeLayout[4]/android.view.View[1]/android.widget.RelativeLayout[2]/android.widget.FrameLayout[1]/android.widget.TextView[1]').click()
    d.click(0.9, 0.715)
    return_home()

#关闭或打开指定灯
def close_or_open_specify_light(index):
    if index!= None:
        if index != 2:
            d(text="灯%s"%(index)).click()
            d(text="左键").click()
            d(text="右键").click()
        else:
            d(text="灯%d"%(index)).click()
            #d(text="某按键").click()
    else:
        print("序号有误")
    return_home()

#打开指定窗帘
def open_specify_curtain(index):
    if index!= None:
        d(text="窗帘%s"%(index)).click()
        d(text="打开").click()
    else:
        print("序号有误")
    return_home()

#关闭指定窗帘
def close_specify_curtain(index):
    if index!= None:
        d(text="窗帘%s"%(index)).click()
        d(text="关闭").click()
    else:
        print("序号有误")
    return_home()

#被调用时，设置家居场景为默认状态
def once_nomal_state():
    d(text="场景").click()
    d(text="自定义").click()
    #xpath点击有问题，暂时弃用
    #d.xpath('//*[@resource-id="com.xiaomi.smarthome:id/ca7"]/android.widget.RelativeLayout[5]/android.view.View[1]/android.widget.RelativeLayout[2]/android.widget.FrameLayout[1]/android.widget.TextView[1]').click()
    d.click(0.916, 0.844)
    return_home()


# 构建Socket实例、设置端口号和监听队列大小
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('127.0.0.1',2333))
listener.listen(5)
print('等待客户端连接...')
#——————————————————————————————————————
#第一次运行启动时，清除adb，连接模拟器，打开米家应用
os.system("adb kill-server")
d=u.connect_adb_wifi("127.0.0.1:62001")
d.app_start("com.xiaomi.smarthome")
#——————————————————————————————————————
#鉴于通过ui包无法合理获取到电灯、插座和窗帘的运行状态，目前快速完成方案为python被unity调用运行时，把所有的灯和窗帘设置为关闭、插座为开启状态。
return_home()
once_nomal_state()
#——————————————————————————————————————
# 进入死循环，等待新的客户端连入。一旦有客户端连入，就分配一个线程去做专门处理。然后自己继续等待。
while True:
    client_executor, addr = listener.accept()
    t = threading.Thread(target=message_receiver, args=(client_executor, addr))
    t.start()


    
    