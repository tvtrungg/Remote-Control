import winreg as winreg
from tkinter import *

def DeleteKey(Client):
    Links = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Got the link","utf-8"))
    Reg = Links.split("\\",1)
    
    if Reg[0] == "HKEY_CLASSES_ROOT": linkReg = winreg.HKEY_CLASSES_ROOT
    elif Reg[0] == "HKEY_CURRENT_USER": linkReg = winreg.HKEY_CURRENT_USER
    elif Reg[0] == "HKEY_LOCAL_MACHINE": linkReg = winreg.HKEY_LOCAL_MACHINE
    elif Reg[0] == "HKEY_USERS": linkReg = winreg.HKEY_USERS
    elif Reg[0] == "HKEY_CURRENT_CONFIG": linkReg = winreg.HKEY_CURRENT_CONFIG
    else:
        Client.sendall(bytes("Path dont exist", "utf-8"))
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
        Client.sendall(bytes("Successfully deleted","utf-8"))
        checkdata = Client.recv(1024).decode("utf-8")

    try:
        DeleteRegKey(linkReg, Reg[1])
    except:
        Client.sendall(bytes("Path dont exist", "utf-8"))
        checkdata = Client.recv(1024).decode("utf-8")
        return     
