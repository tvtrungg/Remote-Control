import winreg as winreg
from tkinter import *

def GetValueReg(Client):
    Name = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Confirm","utf-8"))
    Links = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Confirm","utf-8"))
    Reg = Links.split("\\",1)
    check = True
    if Reg[0] == "HKEY_CLASSES_ROOT": linkReg = winreg.HKEY_CLASSES_ROOT
    elif Reg[0] == "HKEY_CURRENT_USER": linkReg = winreg.HKEY_CURRENT_USER
    elif Reg[0] == "HKEY_LOCAL_MACHINE": linkReg = winreg.HKEY_LOCAL_MACHINE
    elif Reg[0] == "HKEY_USERS": linkReg = winreg.HKEY_USERS
    elif Reg[0] == "HKEY_CURRENT_CONFIG": linkReg = winreg.HKEY_CURRENT_CONFIG
    else:
        Client.sendall(bytes("Path dont exist", "utf-8"))
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
            Client.sendall(bytes("Path dont exist", "utf-8"))
            checkdata = Client.recv(1024).decode("utf-8")
   