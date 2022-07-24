import winreg as winreg
from tkinter import *

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
