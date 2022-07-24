import winreg as winreg
from tkinter import *

def DeleteKey(Client):
    Links = Client.recv(1024).decode("utf-8")                           # Nhận đường dẫn từ server
    Client.sendall(bytes("Got the link","utf-8"))                       # Gửi thông điệp đến server
    Reg = Links.split("\\",1)                                           # Tách đường dẫn
    
    if Reg[0] == "HKEY_CLASSES_ROOT": linkReg = winreg.HKEY_CLASSES_ROOT                # Nếu đường dẫn là HKEY_CLASSES_ROOT
    elif Reg[0] == "HKEY_CURRENT_USER": linkReg = winreg.HKEY_CURRENT_USER              # Nếu đường dẫn là HKEY_CURRENT_USER
    elif Reg[0] == "HKEY_LOCAL_MACHINE": linkReg = winreg.HKEY_LOCAL_MACHINE            # Nếu đường dẫn là HKEY_LOCAL_MACHINE
    elif Reg[0] == "HKEY_USERS": linkReg = winreg.HKEY_USERS                            # Nếu đường dẫn là HKEY_USERS
    elif Reg[0] == "HKEY_CURRENT_CONFIG": linkReg = winreg.HKEY_CURRENT_CONFIG          # Nếu đường dẫn là HKEY_CURRENT_CONFIG    
    else:
        Client.sendall(bytes("Path dont exist", "utf-8"))                               # Nếu đường dẫn không tồn tại
        checkdata = Client.recv(1024).decode("utf-8")                                   # Nhận thông điệp từ server
        return
    
    def DeleteRegKey(REG_LINK, REG_PATH):
        REG_KEY = winreg.OpenKey(REG_LINK, REG_PATH ,0, winreg.KEY_ALL_ACCESS)          # Mở đường dẫn
        REG_DATA = winreg.QueryInfoKey(REG_KEY)                                         # Lấy thông tin của đường dẫn
        for registry in range(0, REG_DATA[0]):                                          # Duyệt từng phần tử của đường dẫn
            REG_SUB = winreg.EnumKey(REG_KEY, 0)                                        # Lấy tên của các đường dẫn con
            try:
                winreg.DeleteKey(REG_KEY, REG_SUB)                                      # Xóa đường dẫn con
            except:
                DeleteRegKey(REG_LINK, REG_PATH)                                        # Gọi lại hàm xóa đường dẫn con
        winreg.DeleteKey(REG_KEY,"")                                                    # Xóa đường dẫn
        winreg.CloseKey(REG_KEY)                                                        # Đóng đường dẫn
        access = winreg.ConnectRegistry(None, linkReg)                                  # Kết nối đến đường dẫn
        Client.sendall(bytes("Successfully deleted","utf-8"))                           # Gửi thông điệp đến server
        checkdata = Client.recv(1024).decode("utf-8")                                   # Nhận thông điệp từ server

    try:
        DeleteRegKey(linkReg, Reg[1])                                                   # Gọi hàm xóa đường dẫn
    except:
        Client.sendall(bytes("Path dont exist", "utf-8"))                               # Nếu đường dẫn không tồn tại
        checkdata = Client.recv(1024).decode("utf-8")                                   # Nhận thông điệp từ server
        return     
