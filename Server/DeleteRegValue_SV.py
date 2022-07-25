import winreg as winreg
from tkinter import *

def DeleteRegValue(Client):
    temp = 0
    test = True
    def DeleteTemp(REG_KEY, REG_SUB, Name):
        REG_KEY = winreg.OpenKey(REG_KEY, REG_SUB ,0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(REG_KEY, Name)
        winreg.CloseKey(REG_KEY)
               
    Links = Client.recv(1024).decode("utf-8")
    REG_SUB = Links
    Client.sendall(bytes("Confirm","utf-8"))
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
    Client.sendall(bytes("Confirm","utf-8"))

    if test == True:
        try:
            REG_LINK = winreg.ConnectRegistry(None, linkReg)
            REG_SUB = REG_SUB[temp:]
            DeleteTemp(REG_LINK, REG_SUB, Name)  

        except WindowsError:
            test = False

    Receives = Client.recv(1024).decode("utf-8")
    if test == True:      
        Client.sendall(bytes("Successfully deleted","utf-8"))  
    elif test == False:
        Client.sendall(bytes("Path dont exist", "utf-8"))
    
    Confirmation = Client.recv(1024).decode("utf-8")    
