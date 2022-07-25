import winreg as winreg
from tkinter import *

def SetValue(Client):
    Name = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Confirm","utf-8"))
    Links = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Confirm","utf-8"))
    data_type = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("xac nhan","utf-8"))
    Value = Client.recv(2048).decode("utf-8")
    Client.sendall(bytes("Confirm","utf-8"))

    Reg = Links.split("\\", 1)
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
            Client.sendall(bytes("Path dont exist", "utf-8"))
            checkdata = Client.recv(1024).decode("utf-8")
