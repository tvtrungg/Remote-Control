import winreg as winreg
from tkinter import *

def DeleteRegValue(Client):
    temp = 0
    test = True
    def DeleteTemp(REG_KEY, REG_SUB, Name):
        REG_KEY = winreg.OpenKey(REG_KEY, REG_SUB ,0, winreg.KEY_ALL_ACCESS)        # Mở đường dẫn
        winreg.DeleteValue(REG_KEY, Name)                                           # Xóa giá trị
        winreg.CloseKey(REG_KEY)                                                    # Đóng đường dẫn
               
    Links = Client.recv(1024).decode("utf-8")                                       # Nhận đường dẫn từ server
    REG_SUB = Links                                                                 
    Client.sendall(bytes("Confirm","utf-8"))                                        # Gửi thông điệp đến server
    Key = Links.split("\\",1)                                                       # Lấy đường dẫn từ link
    
    if Key[0] == "HKEY_CLASSES_ROOT":
        temp = 18
        linkReg = winreg.HKEY_CLASSES_ROOT                                          # Nếu đường dẫn là HKEY_CLASSES_ROOT

    elif Key[0] == "HKEY_CURRENT_USER":
        temp = 18
        linkReg = winreg.HKEY_CURRENT_USER                                          # Nếu đường dẫn là HKEY_CURRENT_USER

    elif Key[0] == "HKEY_LOCAL_MACHINE":
        temp = 19
        linkReg = winreg.HKEY_LOCAL_MACHINE                                         # Nếu đường dẫn là HKEY_LOCAL_MACHINE

    elif Key[0] == "HKEY_USERS":
        temp = 11
        linkReg = winreg.HKEY_USERS                                                 # Nếu đường dẫn là HKEY_USERS

    elif Key[0] == "HKEY_CURRENT_CONFIG":
        temp = 20
        linkReg = winreg.HKEY_CURRENT_CONFIG                                        # Nếu đường dẫn là HKEY_CURRENT_CONFIG

    else:
        test = False

    Name = Client.recv(1024).decode("utf-8")                                        # Nhận tên giá trị
    Client.sendall(bytes("Confirm","utf-8"))                                        # Gửi thông điệp đến server

    if test == True:
        try:
            REG_LINK = winreg.ConnectRegistry(None, linkReg)                        # Kết nối đến đường dẫn
            REG_SUB = REG_SUB[temp:]                                                # Lấy đường dẫn từ link
            DeleteTemp(REG_LINK, REG_SUB, Name)                                     # Gọi hàm xóa giá trị

        except WindowsError:
            test = False                                                            # Nếu không tồn tại đường dẫn

    Receives = Client.recv(1024).decode("utf-8")                                        # Nhận thông điệp từ server
    if test == True:                                                                    # Nếu thành công
        Client.sendall(bytes("Successfully deleted","utf-8"))                           # Gửi thông điệp đến server
    elif test == False:                                                                 # Nếu không thành công
        Client.sendall(bytes("Path dont exist", "utf-8"))                               # Gửi thông điệp đến server
    
    Confirmation = Client.recv(1024).decode("utf-8")                                    # Nhận thông điệp từ server
